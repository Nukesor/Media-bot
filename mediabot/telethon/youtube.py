from telethon import events

from mediabot import log, get_peer_information
from mediabot.config import config
from mediabot.telethon import bot
from mediabot.download import (
    download_media,
    Info,
)
from mediabot.telethon.files import handle_file_upload, handle_file_backup


@bot.on(
    events.NewMessage(
        pattern="\\\\music",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def youtube_music(event):
    """Set the media chat."""
    text = event.message.message
    url = text.split(" ")[1]

    info = Info()
    info.type = "audio"
    info.caption = f"Original link: {url}"
    info.youtube_dl = True
    info.youtube_dl_url = url

    try:
        info, media = download_media(info)
        await handle_file_upload(event, info, media)
    except Exception as e:
        log(f"Got exception: {e}")


@bot.on(
    events.NewMessage(
        pattern="\\\\clip",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def youtube_clip(event):
    """Set the media chat."""
    text = event.message.message

    info = Info()
    info.type = "video"
    info.youtube_dl = True
    info.youtube_dl_url = text.split(" ")[1]

    try:
        info, media = download_media(info)
        await handle_file_backup(event, info, media)
        await handle_file_upload(event, info, media)
    except Exception as e:
        log(f"Got exception: {e}")
