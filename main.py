# main.py
import os
from dotenv import load_dotenv

# Load .env first so config.py sees the env vars when it's imported
load_dotenv()

import importlib
import sys
from config import app  # now safe: env vars already loaded

def load_handlers():
    handlers_dir = "handlers"

    if not os.path.isdir(handlers_dir):
        print(f"⚠️ Handlers folder not found: {handlers_dir}")
        return

    # Optional: ensure handlers is importable as a package
    if handlers_dir not in sys.path:
        sys.path.insert(0, os.getcwd())

    for filename in os.listdir(handlers_dir):
        if not filename.endswith(".py"):
            continue
        if filename.startswith("_"):
            # skip private modules like __init__.py or _helper.py
            continue

        module_name = f"{handlers_dir}.{filename[:-3]}"
        try:
            importlib.import_module(module_name)
            print(f"✅ Loaded handler: {module_name}")
        except Exception as e:
            # Print stack trace so logs show the real error
            import traceback
            print(f"❌ Failed to load {module_name}: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    print("🔁 Loading handlers...")
    load_handlers()
    print("📦 Handlers loaded successfully!")
    print("🚀 Starting bot...")
    # Do not print secrets to logs
    try:
        app.run()
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user")
    except Exception as e:
        print("❌ Bot crashed:", e)
        import traceback
        traceback.print_exc()
