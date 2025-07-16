# Spec to Code AI

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Backend-Flask-blue?logo=flask)
![HuggingFace](https://img.shields.io/badge/Model-HuggingFace-yellow?logo=huggingface)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Spec to Code AI is a web application that uses AI to transform natural language feature specifications into clean, secure, working code snippets in a variety of programming languages. The backend leverages HuggingFace code generation models, while the frontend provides a modern, interactive UI for users to input specifications, select a language and model, and receive validated code with language-specific checks.

---

## Features
- Input natural language specifications and select a target programming language.
- Choose between two AI models: `Salesforce/codegen-350M-mono` and `Salesforce/codegen-350M-multi`.
- Generate code using the selected AI model and language.
- Output validation: Ensures generated code matches the requested language (checks for language-specific syntax/keywords).
- User-friendly error messages if the model fails to generate valid code.
- Copy, run, and save generated code (UI supports these actions; backend currently only supports code generation).
- View history of generated code snippets (stored in browser localStorage).
- Modern, responsive UI with a space-themed design.

---

## Supported Languages & Validation
- **Python** (with special validation for Fibonacci function requests)
- **JavaScript**
- **Java**
- **Ruby**
- **Go**
- **C++**
- **C**
- **PHP**

The backend checks for language-specific keywords in the generated code and returns an error if the output does not match the requested language, improving reliability and user experience.

---

## Tech Stack
- **Backend:** Python, Flask, HuggingFace Transformers, PyTorch
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Models:**
  - [Salesforce/codegen-350M-mono](https://huggingface.co/Salesforce/codegen-350M-mono)
  - [Salesforce/codegen-350M-multi](https://huggingface.co/Salesforce/codegen-350M-multi)

---

## Setup Instructions

### Backend

1. **Install Python dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Run the backend server:**
   ```bash
   python backend/app.py
   ```
   The backend will start on `http://localhost:5000`.

### Frontend

1. **Serve the frontend (from the `frontend` directory):**
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   The frontend will be available at `http://localhost:8000`.

---

## Usage

1. Open the frontend in your browser (`http://localhost:8000`).
2. Enter a feature specification (e.g., "Create a Python function that calculates Fibonacci numbers").
3. Select the desired programming language and model.
4. Click "Generate Code" to receive AI-generated code.
5. Use the UI to copy, run (UI only; backend does not execute code), or save the code.

---

## Notes
- The backend only supports code generation. The "Run" button in the UI is present, but there is no `/execute_code` endpoint implemented in the backend.
- The AI models are loaded at backend startup. If model loading fails, the backend will return an error for code generation requests.
- The frontend uses localStorage to keep a history of generated code.
- Output validation is performed for all supported languages to ensure code quality and relevance.
- A system instruction is always prepended to the prompt to encourage clean, secure code generation.

---

## Requirements
- Python 3.8+
- Node.js (optional, only if you want to use a different frontend server)
- Modern web browser

---

## License
MIT License

---

## Credits
- [Salesforce/codegen-350M-mono](https://huggingface.co/Salesforce/codegen-350M-mono)
- [Salesforce/codegen-350M-multi](https://huggingface.co/Salesforce/codegen-350M-multi)
- [HuggingFace Transformers](https://huggingface.co/transformers/)
- [Flask](https://flask.palletsprojects.com/) 
