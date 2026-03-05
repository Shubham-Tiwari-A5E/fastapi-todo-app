#!/usr/bin/env python3
"""
FastAPI Todo App - Production Start Script
For deployment without hot-reload
"""

import sys
import os

def main():
    """Start server in production mode"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("🚀 Starting FastAPI Server (Production Mode)")
    print(f"📁 Directory: {os.getcwd()}")
    print(f"🐍 Python: {sys.version.split()[0]}\n")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            reload=False,
            workers=int(os.getenv("WEB_CONCURRENCY", 1)),
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
