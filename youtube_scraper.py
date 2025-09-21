"""YouTube trailer comment helper functions.

Gracefully degrades when the YOUTUBE_API key is missing by returning
empty results instead of raising errors. This allows the rest of the
application to function in educational / demo contexts without API quota.
"""

from __future__ import annotations

import os
from typing import List, Dict, Optional

from dotenv import load_dotenv

try:  # Import lazily so unit tests without dependency still run
    from googleapiclient.discovery import build  # type: ignore
except Exception:  # pragma: no cover - optional dependency path
    build = None  # type: ignore

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API")
_yt_client = None


def _get_client():
    """Return a cached YouTube API client or None if unavailable."""
    global _yt_client
    if _yt_client is not None:
        return _yt_client
    if not YOUTUBE_API_KEY or not build:
        return None
    try:
        _yt_client = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    except Exception:  # pragma: no cover - network/auth errors
        _yt_client = None
    return _yt_client


def search_trailer_video_id(movie_title: str) -> Optional[str]:
    client = _get_client()
    if not client:
        return None
    search_response = client.search().list(
        q=f"{movie_title} official trailer",
        part="snippet",
        type="video",
        maxResults=1,
    ).execute()
    if not search_response.get("items"):
        return None
    return search_response["items"][0]["id"]["videoId"]


def get_trailer_comments(movie_title: str, max_pages: int = 3) -> List[Dict[str, str]]:
    video_id = search_trailer_video_id(movie_title)
    if not video_id:
        return []
    client = _get_client()
    if not client:
        return []

    comments: List[Dict[str, str]] = []
    next_page_token: Optional[str] = None

    for _ in range(max_pages):
        response = client.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
            order="time",
            pageToken=next_page_token,
        ).execute()

        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({'text': comment.get('textDisplay', '')})
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    comments.reverse()
    return comments
