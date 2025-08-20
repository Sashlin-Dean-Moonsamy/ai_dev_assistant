# app/file_analyzer.py

from pathlib import Path
from app.config import CODE_FOLDER

def load_code_files():
    """
    Reads all code files (.py, .js, .html, .css) recursively from CODE_FOLDER,
    concatenates their content, and returns as a single string.

    Returns:
        str: Combined text content of all code files.
    """
    code_extensions = [".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css"]
    collected_code = ""

    # Walk through all files in code folder and subfolders
    for file_path in CODE_FOLDER.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in code_extensions:
            try:
                content = file_path.read_text(encoding="utf-8")
                collected_code += f"\n\n# File: {file_path.relative_to(CODE_FOLDER)}\n{content}"
            except Exception as e:
                print(f"[FileAnalyzer] Could not read {file_path}: {e}")

    return collected_code
