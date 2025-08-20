# app/utils.py

from datetime import datetime
from app.config import SESSIONS_FOLDER

def save_session_log(user_input, ai_response):
    """
    Append the conversation pair to a markdown log file in SESSIONS_FOLDER,
    filename based on current date.

    Args:
        user_input (str): What the user asked.
        ai_response (str): AI's reply.
    """
    SESSIONS_FOLDER.mkdir(exist_ok=True)
    filename = SESSIONS_FOLDER / f"session_{datetime.now().strftime('%Y%m%d')}.md"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"## User:\n{user_input}\n\n")
        f.write(f"## AI:\n{ai_response}\n\n---\n\n")
