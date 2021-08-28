import json
from base64 import urlsafe_b64decode as b64decode
from typing import Optional

import requests
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from .utils import get_video_urls, heights

app = FastAPI()


@app.get("/video/{video_id_b64}")
def video(video_id_b64: str, height: Optional[int] = 720):
    # Parse video_id and return JSON
    try:
        video_id = b64decode(video_id_b64).decode("ascii")
    except:
        return {"error": "Invalid base64 data"}
    return get_video_urls(video_id, "video", height)


@app.get("/{video_id_b64}")
def audio_video(video_id_b64: str,  height: Optional[int] = 720):
    # Parse video_id and return JSON
    try:
        video_id = b64decode(video_id_b64).decode("ascii")
    except:
        return {"error": "Invalid base64 data"}
    return get_video_urls(video_id, "audio_video", height)


@app.get("/audio/{video_id_b64}")
def audio(video_id_b64):
    try:
        video_id = b64decode(video_id_b64).decode("ascii")
    except:
        return {"error": "Invalid base64 data"}
    return get_video_urls(video_id, "audio")


@app.get("/")
def home():
    return "video -} /video/base64($video_url_id)?height=$height\naudio -} /audio/base64($video_url_id)\naudio + video -} /base64($video_url_id)?height=$height"


@app.get("/proxy/{url}")
def media_proxy(url):
    # Parse url
    url = b64decode(url).decode("ascii")
    print(url)

    # Check if link redirects
    head = requests.head(url, allow_redirects=False)
    if head.status_code == 302:
        url = head.headers["location"]

    # Get data
    resp = requests.get(url, stream=True)
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    # print(headers)
    # Return response
    response = StreamingResponse(
        resp.iter_content(chunk_size=1024), media_type=[header for header in headers if header[0] == "Content-Type"][0][1])
    return response
