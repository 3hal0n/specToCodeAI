from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
import json
import subprocess
import tempfile
import uuid
from datetime import datetime
import requests  # For OpenAI API
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Model setup - Only OpenAI and HuggingFace Inference API are supported now
# Remove local model loading for HuggingFace

# File-based persistence
HISTORY_FILE = "history.json"

def load_history():
    """Load history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading history: {e}")
            return []
    return []

def save_history(history):
    """Save history to JSON file"""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")

@app.route('/generate_code', methods=['POST'])
def generate_code():
    data = request.get_json()
    spec = data.get('spec', '')
    # Ignore provider, always use HuggingFace
    # provider = data.get('provider', 'huggingface')

    if not spec:
        return jsonify({'error': 'No spec provided'}), 400

    # Use HuggingFace Inference API only
    hf_api_key = os.getenv('HF_API_KEY')
    if not hf_api_key:
        return jsonify({'error': 'HuggingFace API key not set in backend environment.'}), 500
    try:
        hf_url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {
            "Authorization": f"Bearer {hf_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": f"# {spec}\n"
        }
        response = requests.post(hf_url, headers=headers, json=payload)
        if response.status_code != 200:
            return jsonify({'error': f'HuggingFace API error: {response.text}'}), 500
        result = response.json()
        # HuggingFace API returns a list of dicts with 'generated_text'
        if isinstance(result, list) and 'generated_text' in result[0]:
            code = result[0]['generated_text']
        else:
            code = str(result)
    except Exception as e:
        return jsonify({'error': f'HuggingFace API call failed: {e}'}), 500

    # Track prompt and output with timestamp
    entry = {
        'id': str(uuid.uuid4()),
        'spec': spec, 
        'code': code.strip(),
        'timestamp': datetime.now().isoformat(),
        'provider': 'huggingface'
    }
    history = load_history()
    history.append(entry)
    save_history(history)
    return jsonify({'code': code.strip()})

@app.route('/execute_code', methods=['POST'])
def execute_code():
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', 'python')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    try:
        if language == 'python':
            return execute_python_code(code)
        elif language == 'javascript':
            return execute_javascript_code(code)
        else:
            return jsonify({'error': f'Language {language} not supported for execution'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def execute_python_code(code):
    """Execute Python code safely"""
    temp_file = None
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Execute with timeout and capture output
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        if result.returncode == 0:
            return jsonify({'output': result.stdout})
        else:
            return jsonify({'error': result.stderr})
            
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Code execution timed out'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except OSError:
                pass  # File might already be deleted

def execute_javascript_code(code):
    """Execute JavaScript code using Node.js"""
    temp_file = None
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Execute with timeout and capture output
        result = subprocess.run(
            ['node', temp_file],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        if result.returncode == 0:
            return jsonify({'output': result.stdout})
        else:
            return jsonify({'error': result.stderr})
            
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Code execution timed out'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except OSError:
                pass  # File might already be deleted

@app.route('/history', methods=['GET'])
def get_history():
    """Get all history entries"""
    history = load_history()
    return jsonify(history)

@app.route('/history/<entry_id>', methods=['GET'])
def get_history_entry(entry_id):
    """Get a specific history entry"""
    history = load_history()
    entry = next((item for item in history if item['id'] == entry_id), None)
    
    if entry:
        return jsonify(entry)
    else:
        return jsonify({'error': 'Entry not found'}), 404

@app.route('/history/<entry_id>', methods=['DELETE'])
def delete_history_entry(entry_id):
    """Delete a specific history entry"""
    history = load_history()
    history = [item for item in history if item['id'] != entry_id]
    save_history(history)
    return jsonify({'message': 'Entry deleted'})

@app.route('/history', methods=['DELETE'])
def clear_history():
    """Clear all history"""
    save_history([])
    return jsonify({'message': 'History cleared'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 