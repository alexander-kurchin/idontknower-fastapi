import os

from dotenv import load_dotenv


load_dotenv()

API_SR_TG = os.getenv("SERVER_SR_TG") + "chat/"
API_TTS = os.getenv("SERVER_TTS") + "tts/"
