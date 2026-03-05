import sys
import os

# Add current directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

def main():
    # Get the directory of this script
    PARENT_DIR = os.path.dirname(SCRIPT_DIR)

    # Check if we're using the virtual environment Python
    venv_python = os.path.join(PARENT_DIR, 'fastapienv', 'Scripts', 'python.exe')
    current_python = sys.executable

    if os.path.normpath(current_python) != os.path.normpath(venv_python):
        print("❌ ERROR: Not using virtual environment Python!")
        print(f"   Current: {current_python}")
        print(f"   Expected: {venv_python}")
        print("")
        print("Please run:")
        print(f'   {venv_python} run.py')
        print("")
        print("Or use start.bat instead")
        input("Press ENTER to exit...")
        sys.exit(1)

    print("🚀 Starting FastAPI Todo Application...")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🐍 Python: {sys.version}")
    print(f"✅ Using virtual environment: {venv_python}")

    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except Exception as e:
        print(f"⚠️ Error loading .env: {e}")
        print("Continuing anyway...")

    try:
        import uvicorn
        print("✅ Uvicorn imported")

        print("\n" + "="*50)
        print("🌟 Server starting on http://127.0.0.1:8000")
        print("🌟 API Docs: http://127.0.0.1:8000/docs")
        print("="*50 + "\n")

        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress ENTER to exit...")

if __name__ == '__main__':
    main()
