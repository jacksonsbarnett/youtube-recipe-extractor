"""Fetch transcripts from YouTube videos."""

import re
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """Extract the video ID from a YouTube URL.

    Supports formats:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
    """
    parsed = urlparse(url)

    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        if parsed.path == "/watch":
            qs = parse_qs(parsed.query)
            if "v" in qs:
                return qs["v"][0]
        elif parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]
    elif parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")

    raise ValueError(f"Could not extract video ID from URL: {url}")


def fetch_transcript(url: str) -> str:
    """Fetch the English transcript for a YouTube video and return as plain text.

    Args:
        url: A YouTube video URL.

    Returns:
        The full transcript as a single string.

    Raises:
        ValueError: If the video ID cannot be extracted.
        TranscriptsDisabled: If the video has no available transcripts.
        NoTranscriptFound: If no English transcript is available.
    """
    video_id = extract_video_id(url)
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=["en"])

    return " ".join(snippet.text for snippet in transcript)
