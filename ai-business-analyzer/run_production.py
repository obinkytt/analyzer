#!/usr/bin/env python3
"""
Production startup script for the AI Business Analyzer
Optimized for cloud deployment
"""
import os
import sys

# Add the current directory to Python path so 'app' module can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment (cloud platforms set this)
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting AI Business Analyzer in production mode...")
    print(f"🌐 Server will be available at http://{host}:{port}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,  # Disable reload in production
        log_level="info",
        access_log=True
    )