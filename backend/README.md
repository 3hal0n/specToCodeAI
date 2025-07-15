# Spec-to-Code AI Flask Backend

This backend provides a code generation API using a lightweight Hugging Face model.

## Requirements
- Python 3.8+
- pip

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (First run) The model will be downloaded automatically on startup (ensure you have internet access).

## Running the Server
```bash
python app.py
```
The server will start on `http://localhost:5000`.

## API Usage
### POST /generate-code
- **Request Body:**
  ```json
  { "spec": "create a login form using HTML and CSS" }
  ```
- **Response:**
  ```json
  { "code": "<generated code>" }
  ```
- **Errors:**
  - Returns helpful error messages if the model fails to load or input is invalid.

## CORS
- CORS is enabled for `http://localhost:3000` (React frontend).

## Model
- Uses `Salesforce/codegen-350M-mono` (Python, <3GB, fast, suitable for prototyping).
- You can change the model in `app.py` by editing `MODEL_NAME`. 