import asyncio
import os
import re
import time
import yt_dlp
import aiohttp
import logging
from typing import Union
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch, Playlist

# ----------------- CONFIGURATION -----------------
DOWNLOAD_DIR = "downloads"
LOGGER = logging.getLogger(__name__)

# --- Shruti API ---
API_URL = os.environ.get("SHRUTI_API_URL", "https://api.shrutibots.site")
API_KEY = os.environ.get("SHRUTI_API_KEY", "ShrutiBotsC0WH1GowF2HkGoKv4F3y")

def time_to_seconds(time_str):
    stringt = str(time_str)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

def get_safe_filename(title: str, default_id: str) -> str:
    if not title:
        return default_id
    return re.sub(r'[\\/*?:"<>|]', "", title).strip()

def extract_video_id(link: str) -> str:
    if "youtu.be/" in link:
        return link.split("youtu.be/")[1].split("?")[0]
    elif "v=" in link:
        return link.split("v=")[1].split("&")[0]
    return link

async def _async_run(func, *args, **kwargs):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

# ----------------- DOWNLOADERS -----------------

async def download_via_shruti(video_id: str, download_type: str, file_path: str) -> str:
    """Shruti API का उपयोग करके डाउनलोड करने का फंक्शन[span_1](start_span)[span_1](end_span)"""
    type_param = "audio" if download_type == "audio" else "video"
    params = {"url": video_id, "type": type_param, "api_key": API_KEY}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/download", params=params, timeout=120) as resp:
                if resp.status == 200:
                    with open(file_path, "wb") as f:
                        async for chunk in resp.content.iter_chunked(131072):
                            f.write(chunk)
                    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                        return file_path
    except Exception as e:
        LOGGER.error(f"Shruti API Download Failed: {e}")
    return None

async def ytdl_fallback_download(link: str, download_type: str, title: str = None) -> str:
    """yt-dlp फॉलबैक डाउनलोडर[span_2](start_span)[span_2](end_span)"""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    video_id = extract_video_id(link)
    filename = get_safe_filename(title, video_id)
    ext = "mp4" if download_type == "video" else "mp3"
    file_path = os.path.join(DOWNLOAD_DIR, f"{filename}.{ext}")

    ydl_opts = {
        'format': 'bestaudio/best' if download_type == "audio" else 'best',
        'outtmpl': file_path,
        'quiet': True,
    }
    
    if download_type == "audio":
        ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]

    try:
        await _async_run(yt_dlp.YoutubeDL(ydl_opts).download, [link])
        return file_path if os.path.exists(file_path) else None
    except Exception as e:
        LOGGER.error(f"yt-dlp error: {e}")
        return None

async def download_song(link: str, title: str = None) -> str:
    video_id = extract_video_id(link)
    file_path = os.path.join(DOWNLOAD_DIR, f"{get_safe_filename(title, video_id)}.mp3")
    
    # 1. Shruti API Try करें
    result = await download_via_shruti(video_id, "audio", file_path)
    if result: return result
    
    # 2. Fallback
    return await ytdl_fallback_download(link, "audio", title)

async def download_video(link: str, title: str = None) -> str:
    video_id = extract_video_id(link)
    file_path = os.path.join(DOWNLOAD_DIR, f"{get_safe_filename(title, video_id)}.mp4")
    
    result = await download_via_shruti(video_id, "video", file_path)
    if result: return result
    
    return await ytdl_fallback_download(link, "video", title)

# ----------------- YOUTUBE API CLASS -----------------

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="

    async def download(self, link: str, mystic, video=False, title=None) -> str:
        if video:
            path = await download_video(link, title=title)
        else:
            path = await download_song(link, title=title)
        return path, bool(path)

YouTube = YouTubeAPI()
