import sys
import os

# Add current directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

if __name__ == '__main__':
    print("🚀 Starting FastAPI Todo Application (No Reload Mode)...")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🐍 Python: {sys.version}")

    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except ImportError:
        print("⚠️  python-dotenv not available, using OS environment only")
    except Exception as e:
        print(f"⚠️  Error loading .env: {e}")

    try:
        import uvicorn
        print("✅ Uvicorn imported")

        print("\n" + "="*50)
        print("🌟 Server starting on http://127.0.0.1:8000")
        print("🌟 API Docs: http://127.0.0.1:8000/docs")
        print("🌟 NO AUTO-RELOAD (restart manually for changes)")
        print("="*50 + "\n")

        # Run WITHOUT reload to avoid multiprocessing issues
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)

    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress ENTER to exit...")
