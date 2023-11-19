import requests

from .api import API_SR_TG


def get_text(voice):
    r = requests.post(API_SR_TG, files={"file": voice})
    prompt = r.json()["prompt"]
    text = r.json()["response"]
    if text.isdigit():
        text = "Чудесный сегодня денёк!"
    return prompt.strip(), text.strip()
