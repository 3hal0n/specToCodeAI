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
        prompt = f"{system_instruction}Write only the {language} code for the following specification. Do not include explanations, comments, or code in other languages: {spec}"
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
        # Output validation for PHP
        if language.lower() == 'php' and '<?php' not in code:
            return jsonify({'error': 'The model did not generate valid PHP code. Please try again or rephrase your specification.'}), 500
        # Output validation for Python (fibonacci)
        if language.lower() == 'python' and 'fibonacci' in spec.lower():
            if 'def' not in code or 'fibonacci' not in code:
                return jsonify({'error': 'The model did not generate a valid Python Fibonacci function. Please try again or rephrase your specification.'}), 500
        # Output validation for JavaScript
        if language.lower() == 'javascript' and not any(kw in code for kw in ['function', '=>', 'const', 'let', 'var']):
            return jsonify({'error': 'The model did not generate valid JavaScript code. Please try again or rephrase your specification.'}), 500
        # Output validation for Java
        if language.lower() == 'java' and not any(kw in code for kw in ['public class', 'public static void main']):
            return jsonify({'error': 'The model did not generate valid Java code. Please try again or rephrase your specification.'}), 500
        # Output validation for Ruby
        if language.lower() == 'ruby' and not ('def' in code and 'end' in code):
            return jsonify({'error': 'The model did not generate valid Ruby code. Please try again or rephrase your specification.'}), 500
        # Output validation for Go
        if language.lower() == 'go' and not any(kw in code for kw in ['package main', 'func']):
            return jsonify({'error': 'The model did not generate valid Go code. Please try again or rephrase your specification.'}), 500
        # Output validation for C++
        if language.lower() == 'cpp' and not any(kw in code for kw in ['#include', 'int main']):
            return jsonify({'error': 'The model did not generate valid C++ code. Please try again or rephrase your specification.'}), 500
        # Output validation for C
        if language.lower() == 'c' and not any(kw in code for kw in ['#include', 'int main']):
            return jsonify({'error': 'The model did not generate valid C code. Please try again or rephrase your specification.'}), 500
        return jsonify({'code': code.strip()})
    except Exception as e:
        return jsonify({'error': f'Code generation failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 