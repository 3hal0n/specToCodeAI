# Spec to Code AI

Spec to Code AI is a web application that uses AI to transform natural language specifications into working code snippets in various programming languages. The backend leverages a HuggingFace code generation model, while the frontend provides a modern, interactive UI for users to input specifications, select a language, and receive generated code.

---

## Features
- Input natural language specifications and select a target programming language.
- Generate code using an AI model (Salesforce/codegen-350M-mono).
- Copy, run, and save generated code (UI supports these actions; backend currently only supports code generation).
- View history of generated code snippets.
- Modern, responsive UI with a space-themed design.

---

## Tech Stack
- **Backend:** Python, Flask, HuggingFace Transformers, PyTorch
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Model:** Salesforce/codegen-350M-mono

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
2. Enter a specification (e.g., "Create a Python function that calculates Fibonacci numbers").
3. Select the desired programming language.
4. Click "Generate Code" to receive AI-generated code.
5. Use the UI to copy, run (UI only; backend does not execute code), or save the code.

---

## Notes
- The backend only supports code generation. The "Run" button in the UI is present, but there is no `/execute_code` endpoint implemented in the backend.
- The AI model is loaded at backend startup. If model loading fails, the backend will return an error for code generation requests.
- The frontend uses localStorage to keep a history of generated code.

---

## Requirements
- Python 3.8+
- Node.js (optional, only if you want to use a different frontend server)
- Modern web browser

---

## License
MIT (or specify your license)

---

## Credits
- [Salesforce/codegen-350M-mono](https://huggingface.co/Salesforce/codegen-350M-mono)
- [HuggingFace Transformers](https://huggingface.co/transformers/)
- [Flask](https://flask.palletsprojects.com/) 