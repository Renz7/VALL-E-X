#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/11/13 18:56
Author  : ren
"""
import logging
import sys
import tempfile
import time
from logging import getLogger

import uvicorn
from fastapi import UploadFile, FastAPI, Form
from fastapi.responses import FileResponse
from scipy.io.wavfile import write as write_wav

from utils.generation import preload_models, generate_audio, SAMPLE_RATE
from utils.prompt_making import make_prompt

logger = getLogger(__file__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.addHandler(logging.FileHandler("log.txt", encoding="utf-8"))
logger.setLevel(logging.INFO)

logger.info("start preload models")
preload_models()
logger.info("preload models done")

app = FastAPI()


@app.post("/voice_clone")
async def voice_clone(prompt_audio: UploadFile, prompt_text: str = Form(), transcript: str = None):
    logger.info("start making prompt")
    prompt_name = f"prompt-{time.time()}"
    tmpfp = tempfile.mktemp(suffix=".wav", prefix="VALL-E-X-")
    with open(tmpfp, "wb") as f:
        f.write(await prompt_audio.read())
        f.flush()
    make_prompt(prompt_name, tmpfp, None)
    logger.info("prompt %s made, start generate audio", prompt_name)
    wav_array = generate_audio(prompt_text, prompt=prompt_name)
    write_wav(tmpfp + ".out", SAMPLE_RATE, wav_array)
    logger.info("audio generated, start streaming")
    return FileResponse(tmpfp + ".out", filename="out.wav")


@app.get("/health")
def health():
    return "ok"


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8001, root_path="/tts")
