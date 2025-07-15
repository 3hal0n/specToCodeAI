#!/usr/bin/env python3
"""
Startup script for Spec to Code AI
Runs both backend and frontend servers
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread, Timer

def run_backend():
    """Run the Flask backend server with AI model"""
    print("Starting backend server with HuggingFace (distilgpt2) and OpenAI support...")
    backend_dir = os.path.join(os.getcwd(), 'backend')
    subprocess.run([sys.executable, 'app.py'], cwd=backend_dir)

def run_frontend():
    """Run the frontend HTTP server"""
    print("Starting frontend server...")
    frontend_dir = os.path.join(os.getcwd(), 'frontend')
    subprocess.run([sys.executable, '../server.py'], cwd=frontend_dir)

def open_browser():
    """Open browser after a delay"""
    webbrowser.open_new('http://localhost:8000')

def main():
    print("🚀 Starting Spec to Code AI")
    print("=" * 60)
    print("🤖 Using HuggingFace distilgpt2 (local, ~500MB) or OpenAI GPT-3.5-turbo (API)")
    print("📦 distilgpt2 will download on first run (~500MB, fast)")
    print("🔑 To use OpenAI, set OPENAI_API_KEY in your .env file")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('backend') or not os.path.exists('frontend'):
        print("❌ Error: Please run this script from the project root directory")
        print("   Make sure you're in the specToCodeAI folder")
        sys.exit(1)
    
    # Start backend in a separate thread
    backend_thread = Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Start frontend in a separate thread
    frontend_thread = Thread(target=run_frontend, daemon=True)
    frontend_thread.start()
    
    # Open browser after delay
    Timer(5, open_browser).start()
    
    print("✅ Servers starting...")
    print("📱 Frontend: http://localhost:8000")
    print("🔧 Backend:  http://localhost:5000")
    print("🌐 Browser will open automatically")
    print("\nPress Ctrl+C to stop all servers")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        sys.exit(0)

if __name__ == '__main__':
    main() 