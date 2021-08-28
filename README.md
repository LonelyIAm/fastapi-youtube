# fastapi-youtube-dl
A FastApi API to get json info about youtube video

## Run server
```bash
#Production
uvicorn app.main:app

#Development
uvicorn app.main:app --reload
```

## Video src

```GET /video/base64($video_id)?height=$height```
```json
{
  "channel": "chanel name",
  "channel_pfp": "channel's profile picture",
  "channel_url": "channel's url",
  "thumbnail": "thumbnail",
  "title": "video title",
  "video": "/proxt/base64($video_url)", // To bypass cors
  "view_count": "view_count"
}
```

## Audio src
```GET /audio/base64($video_id)```
```json
{
  "channel": "chanel name",
  "channel_pfp": "channel's profile picture",
  "channel_url": "channel's url",
  "thumbnail": "thumbnail",
  "title": "video title",
  "audio": "/proxt/base64($audio_url)", // To bypass cors
  "view_count": "view_count"
}
```

## Audio and video src
```GET /base64(video_id)?height=height```
```json
{
  "channel": "chanel name",
  "channel_pfp": "channel's profile picture",
  "channel_url": "channel's url",
  "thumbnail": "thumbnail",
  "title": "video title",
  "video": "/proxt/base64($video_url)", // To bypass cors
  "audio": "/proxt/base64($audio_url)", // To bypass cors
  "view_count": "view_count"
}
```
if the video has a url that contains both video and audio, the API returns this 
```json
{
  "channel": "chanel name",
  "channel_pfp": "channel's profile picture",
  "channel_url": "channel's url",
  "thumbnail": "thumbnail",
  "title": "video title",
  "audio_video": "/proxt/base64($audio_video_url)", // To bypass cors
  "view_count": "view_count"
}
```

## Proxy route
The route streams the contents of the $url, this is to bypass CORS policy of the original $url and use it in javascript webapps

```GET /proxy/base64($url)```
