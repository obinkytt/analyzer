#!/usr/bin/env python3
"""
Simple startup script for the AI Business Analyzer
"""
import os
import sys
import webbrowser
import threading
import time

# Add the current directory to Python path so 'app' module can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def open_browser():
    """Open the browser after a short delay to ensure server is running"""
    time.sleep(2)  # Wait 2 seconds for server to start
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    import uvicorn
    
    # Start browser opening in background
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("🚀 Starting AI Business Analyzer...")
    print("📱 Opening browser at http://127.0.0.1:8000")
    print("⏹️  Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )