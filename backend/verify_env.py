from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / '.env'

print(f"Checking for .env at: {ENV_PATH}")
if ENV_PATH.exists():
    print(".env file FOUND")
else:
    print(".env file NOT FOUND")

load_dotenv(ENV_PATH)

key = os.environ.get('GEMINI_API_KEY')
if key:
    print(f"SUCCESS: Key loaded (starts with {key[:5]}...)")
else:
    print("FAILURE: Key NOT loaded")
