"""Media url link handling logic."""

import os
import secrets
import subprocess

import yt_dlp
from yt_dlp.utils import sanitize_filename

from mediabot import log
from mediabot.media_info import Adapter, Info, TargetFormat


def download_media(info) -> tuple[Info, bytes]:
    """Download media via yt-dlp based on the given info.

    yt-dlp can handle both video and audio.
    """
    if info.adapter != Adapter.Ytdlp:
        raise Exception(
            f"Got media that was supposed to be handled by another adapter: {info.adapter}"
        )

    if info.target_format == TargetFormat.Mp4 or info.target_format == TargetFormat.Webm:
        log("--- Download video via yt-dlp")
        media = download_youtube_media(info)
        return info, media

    elif info.target_format == TargetFormat.Mp3:
        log("--- Download music via yt-dlp")
        media = download_youtube_music(info)
        return info, media
    else:
        raise Exception(f"--- Got unexpected target format: {info.target_format}")


def download_youtube_media(info: Info) -> bytes:
    """Try to download a clip via yt-dlp."""
    # Create a temporary working dir, in case it doesn't already exist.
    if not os.path.exists("/tmp/mediabot"):
        os.mkdir("/tmp/mediabot")

    # Instruct yt-dlp to download the file to a temporary file.
    random_hash = secrets.token_hex(nbytes=8)
    hash = "reddit_" + random_hash
    options = {
        "outtmpl": f"/tmp/mediabot/{hash}_%(title)s.%(ext)s",
        "quiet": True,
        "restrictfilenames": True,
    }

    ydl = yt_dlp.YoutubeDL(options)
    yd_info = ydl.extract_info(info.url)

    # Remove invalid chars that are removed from the title by youtube
    info.title = sanitize_filename(yd_info["title"], True)
    log(f"--- Info: {info}")
    path = f"/tmp/mediabot/{hash}_{info.file_name()}"

    # This is the path where yt-dlp will put its file
    temp_path = f"/tmp/mediabot/{hash}_{info.title}.{yd_info['ext']}"

    # yt-dlp might produce mkv containers, if the downloaded formats don't match
    # There's sadly no indicator for this is happening except the mkv file being present.
    # Check if the target file doesn't exist as mp4, but rather as mkv.
    # If that's the case, convert to mp4 via ffmpeg
    mkv_path = f"/tmp/mediabot/{hash}_{info.title}.mkv"
    if not os.path.exists(temp_path) and os.path.exists(mkv_path):
        temp_path = mkv_path

    # If the format/extension doesn't match up, convert it via ffmpeg.
    if temp_path != path:
        command = ["ffmpeg", "-i", temp_path, "-c", "copy", path]
        print(f"Running command: {command}")
        result = subprocess.run(command, capture_output=True)
        if result.returncode != 0:
            print(result.stdout.decode("utf-8"))
            print(result.stderr.decode("utf-8"))
            raise Exception("Format conversion via ffmpeg failed!")
        os.remove(temp_path)

    # Read and remove the oiginal files
    with open(path, "rb") as file:
        media = file.read()
    os.remove(path)

    log("--- Got media")

    return media


def download_youtube_music(info: Info) -> bytes:
    """Try to extract the audio of a clip via yt-dlp."""
    # Create a temporary working dir, in case it doesn't already exist.
    if not os.path.exists("/tmp/mediabot"):
        os.mkdir("/tmp/mediabot")

    # Instruct yt-dlp to download the file as audio-only to a temporary file.
    random_hash = secrets.token_hex(nbytes=8)
    hash = "reddit_" + random_hash
    options = {
        "outtmpl": f"/tmp/mediabot/{hash}_%(title)s.%(ext)s",
        "quiet": True,
        "format": "bestaudio",
        "restrictfilenames": True,
    }

    ydl = yt_dlp.YoutubeDL(options)
    yd_info = ydl.extract_info(info.url)

    # Remove invalid chars that are removed from the title by youtube
    info.title = sanitize_filename(yd_info["title"], True)
    log(f"--- Info: {info}")

    # If the exported file isn't in the requested format, convert it via ffmpeg.
    temp_path = f"/tmp/mediabot/{hash}_{info.title}.{yd_info['ext']}"
    target_path = f"/tmp/mediabot/{hash}_{info.file_name()}"
    if temp_path != target_path:
        command = ["ffmpeg", "-i", temp_path, "-q:a", "0", "-map", "a", target_path]
        print(f"Running command: {command}")
        result = subprocess.run(
            command,
            capture_output=True,
        )
        if result.returncode != 0:
            print(result.stdout.decode("utf-8"))
            print(result.stderr.decode("utf-8"))
            raise Exception("Format conversion via ffmpeg failed!")
        os.remove(temp_path)

    # Read and remove the oiginal files
    with open(target_path, "rb") as file:
        media = file.read()
    os.remove(target_path)

    return media
