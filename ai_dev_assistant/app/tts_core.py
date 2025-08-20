# app/tts_core.py

import os
import tempfile
import sounddevice as sd
import numpy as np
from TTS.api import TTS
from app.config import VOICES_FOLDER

class VoiceAssistant:
    def __init__(self):
        """
        Initialize the TTS engine.
        Downloads the default English voice model if not present.
        """
        print("[TTS] Initializing voice engine...")
        # You can change this model to any other supported by Coqui TTS
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
        print("[TTS] Voice engine ready.")

    def speak(self, text):
        """
        Convert text to speech and play it immediately.

        Args:
            text (str): Text to be spoken aloud.
        """
        print(f"[TTS] Speaking: {text}")
        # Generate waveform (numpy array) from text
        wav = self.tts.tts(text)

        # Play audio using sounddevice
        sd.play(wav, samplerate=self.tts.synthesizer.output_sample_rate)
        sd.wait()
