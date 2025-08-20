# app/config.py

from pathlib import Path

# Root folder
ROOT_DIR = Path(__file__).parent.parent

# Model folder path
MODEL_PATH = ROOT_DIR / "models" / "mistral-7b-instruct-v0.3"

# Data folders for code/images
CODE_FOLDER = ROOT_DIR / "data" / "code"
IMAGES_FOLDER = ROOT_DIR / "data" / "images"

# Sessions folder to save chat logs
SESSIONS_FOLDER = ROOT_DIR / "sessions"

# Voices folder for TTS audio cache
VOICES_FOLDER = ROOT_DIR / "voices"
