import requests

from .api import API_TTS


def get_audio(text="Привет!"):
    r = requests.get(API_TTS, params={"text": text})
    return r.content
