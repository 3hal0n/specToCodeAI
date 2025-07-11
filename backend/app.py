from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import os

app = Flask(__name__)

# Model setup
CHECKPOINT = "bigcode/starcoder2-3b"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Use quantization if on limited hardware
quantization_config = BitsAndBytesConfig(load_in_8bit=True)
tokenizer = AutoTokenizer.from_pretrained(CHECKPOINT)
model = AutoModelForCausalLM.from_pretrained(
    CHECKPOINT,
    quantization_config=quantization_config,
).to(DEVICE)

# Simple in-memory history (replace with DB/file for persistence)
history = []

@app.route('/generate_code', methods=['POST'])
def generate_code():
    data = request.get_json()
    spec = data.get('spec', '')
    if not spec:
        return jsonify({'error': 'No spec provided'}), 400

    # Prepare prompt for StarCoder2 (not instruction-tuned, so use code-style prompt)
    prompt = f"""# {spec}\n"""
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(DEVICE)
    outputs = model.generate(inputs, max_new_tokens=256, do_sample=True, temperature=0.7)
    code = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Track prompt and output
    entry = {'spec': spec, 'code': code}
    history.append(entry)

    return jsonify({'code': code})

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 