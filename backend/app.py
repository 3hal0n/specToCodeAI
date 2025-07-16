from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging

app = Flask(__name__)
CORS(app, resources={r"/generate-code": {"origins": "http://localhost:8000"}})

MONO_MODEL_NAME = "Salesforce/codegen-350M-mono"
MULTI_MODEL_NAME = "Salesforce/codegen-350M-multi"
mono_tokenizer = None
mono_generator = None
multi_tokenizer = None
multi_generator = None
load_error = None

try:
    mono_tokenizer = AutoTokenizer.from_pretrained(MONO_MODEL_NAME)
    mono_generator = AutoModelForCausalLM.from_pretrained(MONO_MODEL_NAME)
    multi_tokenizer = AutoTokenizer.from_pretrained(MULTI_MODEL_NAME)
    multi_generator = AutoModelForCausalLM.from_pretrained(MULTI_MODEL_NAME)
except Exception as e:
    load_error = str(e)
    logging.error(f"Model loading failed: {load_error}")

@app.route('/generate-code', methods=['POST'])
def generate_code():
    if load_error:
        return jsonify({'error': f'Model loading failed: {load_error}'}), 500
    data = request.get_json()
    spec = data.get('spec', '')
    language = data.get('language', 'python')
    model = data.get('model', MONO_MODEL_NAME)
    # Input sanitization
    if not isinstance(spec, str) or not spec.strip():
        return jsonify({'error': 'Invalid or empty specification.'}), 400
    if len(spec) > 512:
        return jsonify({'error': 'Specification too long (max 512 characters).'}), 400
    try:
        system_instruction = (
            "You are a coding assistant that converts feature specifications into clean, secure code. "
             "Always respond in the requested language and do not include any unrelated content. "
        )
        prompt = f"{system_instruction}Write a {language} function for the following specification: {spec}"
        if model == MULTI_MODEL_NAME:
            tokenizer = multi_tokenizer
            generator = multi_generator
        else:
            tokenizer = mono_tokenizer
            generator = mono_generator
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = generator.generate(
                input_ids,
                max_length=256,
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
                pad_token_id=tokenizer.eos_token_id
            )
        code = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Remove the input prompt from the output if present
        if code.startswith(prompt):
            code = code[len(prompt):].lstrip('\n')
        return jsonify({'code': code.strip()})
    except Exception as e:
        return jsonify({'error': f'Code generation failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 