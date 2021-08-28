from youtube_dl import YoutubeDL
from json import dumps, dump
from requests import get
from base64 import urlsafe_b64encode


ydl = YoutubeDL({"quiet": True})
heights = [
    144,
    240,
    360,
    480,
    720,
    1080,
    1440,
    2160
]

def encode_urls(url: str):
    b64 = urlsafe_b64encode(url.encode("ascii")).decode("ascii")
    return f"/proxy/{b64}"



def get_channel_pfp(url):
    page = get(url).text
    pfp = page.split('{"videoSecondaryInfoRenderer":{"owner":{"videoOwnerRenderer":{"thumbnail":{"thumbnails":[{"url":"')[
        -1].split('"')[0].replace("48", "128")
    return pfp


def get_audio(formats):
    format = [format for format in formats if format.get(
        "vcodec") == "none" and format.get("acodec") != "none"]

    if format:
        return {"audio": encode_urls(format[0].get("url"))}

    return {"audio": None}


def get_video(formats, height):
    format = [format for format in formats if format.get("vcodec") != "none" and format.get(
        "acodec") == "none" and format.get("format_note") == str(height) + "p"]

    i = heights.index(height)
    while(not format and i > 0):
        format = [format for format in formats if format.get("vcodec") != "none" and format.get(
            "acodec") == "none" and format.get("format_note") == str(heights[i]) + "p"]
        i -= 1

    if format:
        return {"video": encode_urls(format[0].get("url"))}

    return {"video": None}


def get_audio_video(formats, height):
    # print(formats)
    format = [format for format in formats if format.get("vcodec") != "none" and format.get(
        "acodec") != "none" and format.get("format_note") == str(height) + "p"]
    if not format:
        video_url = get_video(formats, height)
        audio_url = get_audio(formats)
        return {
            "video": encode_urls(video_url.get("video")),
            "audio": encode_urls(audio_url.get("audio"))
        }

    return {"audio_video": encode_urls(format[0].get("url"))}


def get_video_urls(video_id, file_type, height = 720):
    try:
        # Get video info and formats
        url = f"https://www.youtube.com/watch?v={video_id}"
        info = ydl.extract_info(url, download=False)
        title = info.get("title")
        thumbnail = info.get("thumbnail")
        view_count = info.get("view_count")
        channel = info.get("uploader")
        channel_url = info.get("channel_url")
        formats = info.get("formats")

        # Extract urls from formats based on height and type
        if file_type == "audio":
            reduced_info = get_audio(formats)
        elif file_type == "video":
            reduced_info = get_video(formats, height)
        else:
            reduced_info = get_audio_video(formats, height)

        # Add video info to extracted urls
        reduced_info.update({
            "title": title,
            "thumbnail": thumbnail,
            "view_count": view_count,
            "channel": channel,
            "channel_url": channel_url,
            "channel_pfp": get_channel_pfp(url),
        })

        return reduced_info
    except Exception as e:
        return {
            "error": str(e)
        }


if __name__ == "__main__":
    print(dumps(get_video_urls("https://www.youtube.com/watch?v=32kYH6XZrIo")))
