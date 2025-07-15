# Spec to Code AI

A powerful AI-powered application that transforms natural language specifications into working code. Built with modern web technologies and powered by HuggingFace (distilgpt2, local) or OpenAI (API), this tool provides an intuitive interface for code generation, execution, and management.

## Features

### 🎯 **Core Functionality**
- **Natural Language to Code**: Transform specifications into working code using AI
- **Model Selection**: Choose between a local HuggingFace model (distilgpt2, free) or OpenAI's GPT-3.5-turbo (API key required)
- **Multi-language Support**: Generate code in Python, JavaScript, Java, PHP, Ruby, Go, and more
- **Real-time Code Execution**: Test generated code immediately in a safe environment
- **Code History**: Persistent storage of all generated code with timestamps
- **Modern UI**: Beautiful, responsive interface with dark theme and syntax highlighting

### 🚀 **Advanced Features**
- **Code Execution**: Run Python and JavaScript code safely with timeout protection
- **File Download**: Save generated code to local files
- **Copy to Clipboard**: One-click code copying
- **History Management**: Browse, reload, and manage previous generations
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### 🛡️ **Security & Safety**
- **Sandboxed Execution**: Code runs in isolated temporary files
- **Timeout Protection**: 30-second execution limits prevent infinite loops
- **Error Handling**: Comprehensive error reporting and recovery
- **CORS Support**: Secure cross-origin resource sharing

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for JavaScript code execution)
- 2GB+ RAM (for HuggingFace model loading)
- Stable internet connection (for initial model download or OpenAI API)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd specToCodeAI
   ```

2. **Set up Python environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the application**
   ```bash
   python start.py
   ```
   This will start both backend and frontend servers automatically.
   
   **Note:** First run will download the distilgpt2 model (~500MB) which is much smaller and faster than previous versions. You can also use OpenAI's GPT-3.5-turbo by selecting it in the UI and providing your API key.

## Usage

### Basic Workflow

1. **Enter Specification**: Type your requirements in natural language
   ```
   Create a Python function that calculates the nth Fibonacci number
   ```

2. **Generate Code**: Click "Generate Code" or press Ctrl+Enter

3. **Review & Execute**: 
   - Review the generated code with syntax highlighting
   - Click "Run" to execute the code
   - Click "Copy" to copy to clipboard
   - Click "Save" to download the file

4. **Manage History**: Browse previous generations in the history section

### Example Specifications

**Python Examples:**
```
Create a function to validate email addresses using regex
Write a Python class for a simple calculator with add, subtract, multiply, divide methods
Generate a function that finds the longest palindrome substring
```

**JavaScript Examples:**
```
Create a function to debounce user input events
Write a JavaScript class for a todo list with add, remove, and toggle methods
Generate a function to deep clone objects
```

**Algorithm Examples:**
```
Implement binary search algorithm in Python
Create a function to sort an array using quicksort
Write a function to find all permutations of a string
```

## API Endpoints

### Code Generation
- `POST /generate_code`
  - Body: `{"spec": "your specification", "provider": "huggingface|openai", "openai_api_key": "sk-..."}`
    - `provider` (optional): "huggingface" (default, local, free) or "openai" (requires API key)
    - `openai_api_key` (required if provider is "openai"): Your OpenAI API key
  - Returns: `{"code": "generated code"}`

### Code Execution
- `POST /execute_code`
  - Body: `{"code": "code to execute", "language": "python|javascript"}`
  - Returns: `{"output": "execution result"}` or `{"error": "error message"}`

### History Management
- `GET /history` - Get all history entries
- `GET /history/<id>` - Get specific entry
- `DELETE /history/<id>` - Delete specific entry
- `DELETE /history` - Clear all history

## Architecture

### Frontend (`frontend/`)
- **HTML5**: Semantic markup with modern structure
- **CSS3**: Responsive design with CSS Grid and Flexbox
- **JavaScript**: Vanilla JS with modular architecture
- **Prism.js**: Syntax highlighting for multiple languages
- **Font Awesome**: Icon library for UI elements

### Backend (`backend/`)
- **Flask**: Lightweight Python web framework
- **StarCoder2**: AI model for code generation
- **CORS**: Cross-origin resource sharing support
- **File Persistence**: JSON-based history storage
- **Subprocess**: Safe code execution with timeouts

### Key Features Implementation

#### Code Generation
```python
# Uses StarCoder2 model for code generation
prompt = f"# {spec}\n"
outputs = model.generate(inputs, max_new_tokens=256, temperature=0.7)
```

#### Safe Code Execution
```python
# Temporary file creation and cleanup
with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as f:
    f.write(code)
    result = subprocess.run(['python', f.name], timeout=30)
```

#### History Persistence
```python
# JSON-based file storage
def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)
```

## Configuration

### Environment Variables
- `DEVICE`: Set to "cuda" for GPU acceleration or "cpu" for CPU-only
- `CHECKPOINT`: AI model checkpoint (default: "bigcode/starcoder2-3b")

### Customization
- **Model**: Change `CHECKPOINT` in `backend/app.py` for different AI models
- **Ports**: Modify port numbers in `server.py` and `backend/app.py`
- **Styling**: Edit `frontend/styles.css` for custom themes
- **Languages**: Add new language support in `execute_code()` function

## Troubleshooting

### Common Issues

1. **Model Loading Error**
   - Ensure sufficient RAM (8GB+ recommended)
   - Try CPU-only mode by setting `DEVICE = "cpu"`

2. **Code Execution Fails**
   - Verify Node.js is installed for JavaScript execution
   - Check Python environment and dependencies

3. **CORS Errors**
   - Ensure backend is running on port 5000
   - Verify `flask-cors` is installed

4. **Frontend Not Loading**
   - Check if port 8000 is available
   - Verify all frontend files are in the `frontend/` directory

### Performance Tips

1. **GPU Acceleration**: Use CUDA-compatible GPU for faster model inference
2. **Model Quantization**: Already enabled for memory efficiency
3. **History Management**: Regularly clear old history entries
4. **Browser Caching**: Enable browser caching for static assets

## Development

### Project Structure
```
specToCodeAI/
├── backend/
│   ├── app.py              # Flask backend with StarCoder2 AI model
│   ├── requirements.txt    # Python dependencies
│   └── history.json       # Persistent history storage
├── frontend/
│   ├── index.html         # Main application interface
│   ├── styles.css         # Modern responsive styling
│   └── script.js          # Frontend logic and API calls
├── server.py              # Frontend HTTP server
├── start.py               # Application startup script
├── requirements.txt       # Main project dependencies
├── README.md              # This file
└── venv/                  # Python virtual environment
```

### Adding New Features

1. **New Language Support**:
   - Add execution function in `backend/app.py`
   - Update language detection in `frontend/script.js`

2. **UI Enhancements**:
   - Modify `frontend/styles.css` for styling
   - Update `frontend/index.html` for structure

3. **API Extensions**:
   - Add new routes in `backend/app.py`
   - Update frontend API calls in `frontend/script.js`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **StarCoder2**: AI model by BigCode
- **Flask**: Web framework
- **Prism.js**: Syntax highlighting
- **Font Awesome**: Icon library

---

**Happy Coding! 🚀** 