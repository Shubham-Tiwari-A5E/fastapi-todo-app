#!/usr/bin/env python3
"""
FastAPI Todo App - Start Script
Similar to 'npm run start' for easy application startup
"""

import sys
import os
import subprocess

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════╗
    ║   📝 FastAPI Todo Application           ║
    ║   Production-Ready Task Manager          ║
    ╚══════════════════════════════════════════╝
    """
    print(banner)

def check_environment():
    """Check if virtual environment exists"""
    venv_paths = [
        os.path.join("..", "fastapienv"),
        os.path.join("..", ".venv"),
        os.path.join(".venv"),
        "venv"
    ]
    
    for venv_path in venv_paths:
        if os.path.exists(venv_path):
            return venv_path
    return None

def main():
    """Main entry point"""
    print_banner()
    
    # Get current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version.split()[0]}")
    
    # Check for .env file
    if os.path.exists(".env"):
        print("✅ Environment file found (.env)")
    else:
        print("⚠️  No .env file found, using system environment variables")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except ImportError:
        print("ℹ️  python-dotenv not installed, using system environment only")
    
    print("\n" + "="*50)
    print("🚀 Starting FastAPI Server...")
    print("="*50)
    print(f"\n🌐 Server will be available at:")
    print(f"   • Local:   http://127.0.0.1:8000")
    print(f"   • Docs:    http://127.0.0.1:8000/docs")
    print(f"   • ReDoc:   http://127.0.0.1:8000/redoc")
    print("\n💡 Press CTRL+C to stop the server\n")
    
    try:
        # Start uvicorn
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n📝 Troubleshooting:")
        print("   1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("   2. Check if port 8000 is available")
        print("   3. Verify DATABASE_URL is set in .env file")
        sys.exit(1)

if __name__ == "__main__":
    main()
