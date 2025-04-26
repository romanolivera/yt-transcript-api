import re
import json
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def extract_video_id(url: str):
    patterns = [
        r'(?:https?://)?(?:www\.)?youtu\.be/([A-Za-z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([A-Za-z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([A-Za-z0-9_-]{11})',
    ]
    for p in patterns:
        m = re.match(p, url)
        if m:
            return m.group(1)
    return None

def handler(request):
    if request.method != "POST":
        return {"statusCode": 405, "body": json.dumps({"error": "method_not_allowed"})}

    try:
        payload = request.json()
    except:
        return {"statusCode": 400, "body": json.dumps({"error": "invalid_json"})}

    url = payload.get("url")
    if not url:
        return {"statusCode": 400, "body": json.dumps({"error": "missing_url"})}

    vid = extract_video_id(url)
    if not vid:
        return {"statusCode": 400, "body": json.dumps({"error": "invalid_url"})}

    try:
        entries = YouTubeTranscriptApi.get_transcript(vid)
        text = " ".join(item["text"] for item in entries)
        return {"statusCode": 200, "body": json.dumps({"transcript": text})}
    except TranscriptsDisabled:
        return {"statusCode": 404, "body": json.dumps({"error": "transcripts_disabled"})}
    except NoTranscriptFound:
        return {"statusCode":
