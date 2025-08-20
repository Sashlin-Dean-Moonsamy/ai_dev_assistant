# app/ai_core.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from app.config import MODEL_PATH

def build_personality_prompt(user_input):
    """
    Construct the prompt string that instructs the AI assistant
    to behave with a specific personality and style.

    This prompt tells the model to be unfiltered, casual, sometimes swear,
    and helpful in coding, debugging, explanations, and chit-chat.

    Args:
        user_input (str): The message or question from the user.

    Returns:
        str: The complete prompt string ready to be fed to the model.
    """
    prompt = f"""
You are an unfiltered AI assistant who speaks casually, swears, and doesn't hold back.
You help the user with coding, debugging, explanations, and chit-chat.
Be helpful, honest, and a bit funny.

User: {user_input}
AI:
"""
    return prompt

class AIAssistant:
    def __init__(self, model_path=MODEL_PATH):
        """
        Initialize the AI assistant by loading the tokenizer and model.

        Uses 8-bit quantization to reduce VRAM usage (via bitsandbytes),
        and automatically selects GPU if available for faster inference.

        Args:
            model_path (str): Path or identifier for the pretrained model.
        """
        print("[AI] Loading tokenizer and model, this may take a while...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            load_in_8bit=True,             # Use 8-bit weights to save GPU memory
            device_map="auto"              # Auto-select device (GPU/CPU)
        )
        print("[AI] Model loaded successfully.")

    def generate_response(self, prompt, max_tokens=256, temperature=0.7):
        """
        Generate a response from the AI model based on the given prompt.

        Args:
            prompt (str): Full prompt string including personality and user input.
            max_tokens (int): Max tokens to generate in the response.
            temperature (float): Controls randomness; higher = more creative.

        Returns:
            str: The generated AI response text.
        """
        # Encode the prompt string into token IDs and move to model device (GPU/CPU)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        # Generate tokens using the model with sampling and temperature
        with torch.no_grad():
            output_tokens = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,                  # Enable sampling for varied output
                temperature=temperature,         # Controls creativity/randomness
                pad_token_id=self.tokenizer.eos_token_id,  # Padding token ID
                eos_token_id=self.tokenizer.eos_token_id   # End-of-sequence token ID
            )

        # Decode the generated tokens, skipping the original prompt tokens
        response = self.tokenizer.decode(
            output_tokens[0][inputs.input_ids.size(1):],
            skip_special_tokens=True
        )

        return response.strip()  # Remove extra whitespace/newlines
