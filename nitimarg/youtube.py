"""YouTube Data API v3 with the channel's OAuth refresh token (no SDK needed)."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

import httpx

from .config import Config

TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"


def access_token(cfg: Config) -> str:
    if not (cfg.yt_client_id and cfg.yt_client_secret and cfg.yt_refresh_token):
        raise RuntimeError("YouTube OAuth is not configured (NM_YT_* variables)")
    res = httpx.post(TOKEN_URL, data={
        "client_id": cfg.yt_client_id,
        "client_secret": cfg.yt_client_secret,
        "refresh_token": cfg.yt_refresh_token,
        "grant_type": "refresh_token",
    }, timeout=30.0)
    res.raise_for_status()
    return res.json()["access_token"]


def _file_chunks(path: Path, size: int = 4 * 1024 * 1024) -> Iterator[bytes]:
    with open(path, "rb") as fh:
        while chunk := fh.read(size):
            yield chunk


def upload_video(cfg: Config, token: str, path: Path, title: str, description: str, tags: list[str],
                 publish_at: datetime | None = None) -> str:
    """Resumable upload, streamed from disk. Returns the video id."""
    status: dict[str, Any] = {"privacyStatus": cfg.yt_privacy, "selfDeclaredMadeForKids": False}
    if publish_at:  # scheduled publish needs private + publishAt
        status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
                  "publishAt": publish_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    meta = {
        "snippet": {"title": title[:100], "description": description[:4900], "tags": tags,
                    "categoryId": cfg.yt_category_id, "defaultLanguage": "hi",
                    "defaultAudioLanguage": "hi"},
        "status": status,
    }
    headers = {"Authorization": f"Bearer {token}"}
    with httpx.Client(timeout=httpx.Timeout(60.0, write=600.0)) as client:
        init = client.post(f"{UPLOAD}/videos", params={"uploadType": "resumable", "part": "snippet,status"},
                           headers={**headers, "X-Upload-Content-Type": "video/mp4",
                                    "X-Upload-Content-Length": str(os.path.getsize(path))},
                           json=meta)
        init.raise_for_status()
        res = client.put(init.headers["Location"], content=_file_chunks(path),
                         headers={**headers, "Content-Type": "video/mp4",
                                  "Content-Length": str(os.path.getsize(path))})
        res.raise_for_status()
        return res.json()["id"]


def set_thumbnail(token: str, video_id: str, path: Path) -> None:
    """Needs a phone-verified channel; failures are reported, not fatal."""
    with open(path, "rb") as fh:
        res = httpx.post(f"{UPLOAD}/thumbnails/set", params={"videoId": video_id},
                         headers={"Authorization": f"Bearer {token}", "Content-Type": "image/jpeg"},
                         content=fh.read(), timeout=120.0)
    res.raise_for_status()


def add_comment(token: str, video_id: str, text: str) -> str:
    """Post the top comment. The API cannot pin it; pin it once in YouTube Studio."""
    res = httpx.post(f"{API}/commentThreads", params={"part": "snippet"},
                     headers={"Authorization": f"Bearer {token}"},
                     json={"snippet": {"videoId": video_id,
                                       "topLevelComment": {"snippet": {"textOriginal": text}}}},
                     timeout=30.0)
    res.raise_for_status()
    return res.json()["id"]


def playlist_id(token: str, title: str) -> str:
    """Find the channel playlist with this title, creating it when missing."""
    headers = {"Authorization": f"Bearer {token}"}
    page = None
    while True:
        params = {"part": "snippet", "mine": "true", "maxResults": 50}
        if page:
            params["pageToken"] = page
        res = httpx.get(f"{API}/playlists", params=params, headers=headers, timeout=30.0)
        res.raise_for_status()
        body = res.json()
        for item in body.get("items", []):
            if item["snippet"]["title"].strip().lower() == title.strip().lower():
                return item["id"]
        page = body.get("nextPageToken")
        if not page:
            break
    res = httpx.post(f"{API}/playlists", params={"part": "snippet,status"}, headers=headers,
                     json={"snippet": {"title": title}, "status": {"privacyStatus": "public"}},
                     timeout=30.0)
    res.raise_for_status()
    return res.json()["id"]


def add_to_playlist(token: str, playlist: str, video_id: str) -> None:
    res = httpx.post(f"{API}/playlistItems", params={"part": "snippet"},
                     headers={"Authorization": f"Bearer {token}"},
                     json={"snippet": {"playlistId": playlist,
                                       "resourceId": {"kind": "youtube#video", "videoId": video_id}}},
                     timeout=30.0)
    res.raise_for_status()


def trending_titles(token: str, queries: list[str], days: int = 7, per_query: int = 10) -> list[str]:
    """Most-viewed recent videos for each query (weekly sentiment check)."""
    after = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    titles: list[str] = []
    for q in queries:
        res = httpx.get(f"{API}/search", params={
            "part": "snippet", "q": q, "type": "video", "order": "viewCount",
            "publishedAfter": after, "regionCode": "IN", "maxResults": per_query,
        }, headers={"Authorization": f"Bearer {token}"}, timeout=30.0)
        res.raise_for_status()
        titles += [i["snippet"]["title"] for i in res.json().get("items", [])]
    return titles
