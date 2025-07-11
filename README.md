# SpecToCodeAI

A simple tool to generate code from structured software specs using the StarCoder2-3B model.

## Backend Setup

1. **Clone the repo and enter the directory**
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```
4. **Run the backend Flask app:**
   ```bash
   python backend/app.py
   ```

## Endpoints
- `POST /generate_code` with JSON `{ "spec": "Build a login page with email/password validation." }` → returns generated code.
- `GET /history` → returns prompt/output history.

## Model
- Uses [StarCoder2-3B](https://huggingface.co/bigcode/starcoder2-3b) from HuggingFace.
- Requires a GPU for best performance, but can run in 8-bit mode on limited hardware.

## Next Steps
- Add a frontend to input specs and display code.
- Add code execution/testing features.
- Persist history to a file or database. 