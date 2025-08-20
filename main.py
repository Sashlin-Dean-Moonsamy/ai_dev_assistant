# main.py
# CLI
import sys
from app.ai_core import AIAssistant
from app.tts_core import VoiceAssistant
from app.file_analyzer import load_code_files
from app.utils import save_session_log

def main():
    print("🤖 AI Dev Assistant — Ready to rock! (type 'exit' to quit)")

    ai = AIAssistant()
    tts = VoiceAssistant()

    # Pre-load your project code context
    code_context = load_code_files()
    if code_context:
        print("[Context] Loaded your codebase for smarter answers.")

    while True:
        user_input = input("\nYou: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("👋 See you later!")
            sys.exit(0)

        # Combine user input with code context for better replies
        prompt = f"{code_context}\n\nUser: {user_input}\nAI:"

        # Generate AI response
        ai_response = ai.generate_response(prompt)

        # Print and speak response
        print(f"\nAI: {ai_response}")
        tts.speak(ai_response)

        # Save chat session
        save_session_log(user_input, ai_response)

if __name__ == "__main__":
    main()
