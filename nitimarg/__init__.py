"""Niti Marg: automated Hinglish explainer videos with Niti Didi.

Low-RAM pipeline: topic -> script (Ollama Cloud) -> fact check -> voice
(ElevenLabs / Edge-TTS) -> FFmpeg assembly from pre-made poses -> Telegram
approval -> YouTube upload.
"""

__version__ = "0.1.0"
