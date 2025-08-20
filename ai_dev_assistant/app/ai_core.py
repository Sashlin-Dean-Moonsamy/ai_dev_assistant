# app/ai_core.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from app.config import MODEL_PATH

class AIAssistant:
    def __init__(self, model_path=MODEL_PATH):
        """
        Initialize the AI assistant by loading the model and tokenizer.
        Uses 8-bit quantization via bitsandbytes if available for efficiency.
        """
        print("[AI] Loading tokenizer and model, this may take a while...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            load_in_8bit=True,             # Use 8-bit weights to reduce VRAM usage
            device_map="auto"              # Automatically use GPU if available
        )
        print("[AI] Model loaded successfully.")

    def generate_response(self, prompt, max_tokens=256, temperature=0.7):
        """
        Generate a response from the AI given a prompt string.

        Args:
            prompt (str): The input text prompt for the model.
            max_tokens (int): Max number of tokens to generate.
            temperature (float): Sampling temperature for creativity.

        Returns:
            str: The generated response text.
        """
        # Encode prompt to token IDs
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        # Generate output tokens
        with torch.no_grad():
            output_tokens = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=temperature,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        # Decode tokens to text, skipping prompt tokens
        response = self.tokenizer.decode(output_tokens[0][inputs.input_ids.size(1):], skip_special_tokens=True)

        return response
