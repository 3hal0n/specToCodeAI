from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import os
import json
import subprocess
import tempfile
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Model setup - Using a smaller, faster model
CHECKPOINT = "microsoft/DialoGPT-small"  # Much smaller model (~117MB)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Use quantization if on limited hardware
quantization_config = BitsAndBytesConfig(load_in_8bit=True)
tokenizer = AutoTokenizer.from_pretrained(CHECKPOINT)
model = AutoModelForCausalLM.from_pretrained(
    CHECKPOINT,
    quantization_config=quantization_config,
).to(DEVICE)

# File-based persistence
HISTORY_FILE = "history.json"

def load_history():
    """Load history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
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
    if not spec:
        return jsonify({'error': 'No spec provided'}), 400

    # For the smaller model, we'll use a simpler approach
    # Since DialoGPT is not specifically trained for code, we'll provide a basic response
    prompt = f"Write code for: {spec}\n\nHere's the code:\n"
    
    try:
        inputs = tokenizer.encode(prompt, return_tensors="pt").to(DEVICE)
        outputs = model.generate(
            inputs, 
            max_new_tokens=200, 
            do_sample=True, 
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract the generated part (remove the prompt)
        code = generated_text[len(prompt):].strip()
        
        # If the model didn't generate good code, provide a template
        if not code or len(code) < 10:
            code = f"""# {spec}
# This is a template for the requested functionality
# You may need to customize this based on your specific requirements

def example_function():
    \"\"\"
    {spec}
    \"\"\"
    # TODO: Implement the functionality
    pass

# Example usage
if __name__ == "__main__":
    example_function()"""
        
    except Exception as e:
        # Fallback template if model fails
        code = f"""# {spec}
# Generated code template

def main():
    \"\"\"
    {spec}
    \"\"\"
    # TODO: Implement the functionality
    print("Functionality to be implemented")
    return None

if __name__ == "__main__":
    main()"""

    # Track prompt and output with timestamp
    entry = {
        'id': str(uuid.uuid4()),
        'spec': spec, 
        'code': code,
        'timestamp': datetime.now().isoformat()
    }
    
    history = load_history()
    history.append(entry)
    save_history(history)

    return jsonify({'code': code})

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
        
        # Clean up
        os.unlink(temp_file)
        
        if result.returncode == 0:
            return jsonify({'output': result.stdout})
        else:
            return jsonify({'error': result.stderr})
            
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Code execution timed out'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def execute_javascript_code(code):
    """Execute JavaScript code using Node.js"""
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
        
        # Clean up
        os.unlink(temp_file)
        
        if result.returncode == 0:
            return jsonify({'output': result.stdout})
        else:
            return jsonify({'error': result.stderr})
            
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Code execution timed out'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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