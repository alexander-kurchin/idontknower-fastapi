import base64
import time

import nest_asyncio
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import ds.sr_tg_module as sr_tg
import ds.tts_module as tts

nest_asyncio.apply()

PROD_MODE, TEST_MODE = True, False

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat/")
async def chat(voice: UploadFile = File()):
    suffix = str(int(time.time()))
    input_file = f"temp/input_{suffix}.webm"
    output_file = f"temp/output_{suffix}.webm"

    if PROD_MODE:
        try:
            with open(input_file, "wb") as f:
                f.write(voice.file.read())
            with open(input_file, "rb") as f:
                prompt, text = sr_tg.get_text(f)

            audio = tts.get_audio(text)
            with open(output_file, "wb") as f:
                f.write(audio)
            audio_base64 = base64.b64encode(audio)
        except Exception:
            return {}
        else:
            return {
                "status": "ok",
                "response": {
                    "prompt": prompt,
                    "text": text,
                    "audio_base64": b"data:audio/webm;base64," + audio_base64,
                },
            }
    elif TEST_MODE:
        from tests.test_response import test_JSONresponse

        with open(input_file, "wb") as f:
            f.write(voice.file.read())
        return test_JSONresponse()
    else:
        print("Кто ты, воин?")
