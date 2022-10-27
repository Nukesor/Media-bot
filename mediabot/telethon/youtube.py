from telethon import events

from mediabot import log
from mediabot.config import config
from mediabot.download import Info, download_media
from mediabot.telethon import bot
from mediabot.telethon.files import handle_file_backup, handle_file_upload


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
    info.youtube = True
    info.youtube_url = url

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
    await download_clip(event)


@bot.on(
    events.NewMessage(
        pattern="\\\\movie",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def youtube_movie(event):
    """Set the media chat."""
    await download_clip(event)


async def download_clip(event):
    text = event.message.message

    info = Info()
    info.type = "video"
    info.youtube = True
    info.youtube_url = text.split(" ")[1]

    try:
        info, media = download_media(info)
        await handle_file_backup(event, info, media)
        await handle_file_upload(event, info, media)
    except Exception as e:
        log(f"Got exception: {e}")
