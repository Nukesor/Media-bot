from telethon.events import NewMessage

from mediabot.config import config
from mediabot.handlers import reddit
from mediabot.media_info import TargetFormat
from mediabot.telethon import bot


@bot.on(
    NewMessage(
        pattern=".*reddit\\.com.*",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def explicit_reddit_clip(event: NewMessage.Event):
    """Set the media chat."""
    await reddit.handle(event, event.message.message, TargetFormat.Mp4)


@bot.on(
    NewMessage(
        pattern="\\\\r",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def generic_reddit(event: NewMessage.Event):
    """Set the media chat."""
    text = event.message.message
    url = text.split(" ")[1]
    await reddit.handle(event, url, TargetFormat.Mp4)
