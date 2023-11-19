import json


def test_JSONresponse():
    with open("tests/response.json", "rb") as f:
        return json.loads(f.read())
