from telethon.events import NewMessage

from mediabot.config import config
from mediabot.handlers import youtube
from mediabot.media_info import TargetFormat
from mediabot.telethon import bot


@bot.on(
    NewMessage(
        pattern="\\\\a",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def youtube_music(event: NewMessage.Event):
    """Set the media chat."""
    await youtube.handle(event, TargetFormat.Mp3)


@bot.on(
    NewMessage(
        pattern="\\\\c",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def youtube_clip(event: NewMessage.Event):
    """Set the media chat."""
    await youtube.handle(event, TargetFormat.Mp4)


@bot.on(
    NewMessage(
        pattern="\\\\m",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def youtube_movie(event: NewMessage.Event):
    """Set the media chat."""
    await youtube.handle(event, TargetFormat.Mp4)
