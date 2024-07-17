from telethon.events import NewMessage

from mediabot.config import config
from mediabot.handlers import reddit
from mediabot.media_info import TargetFormat
from mediabot.telethon import bot


@bot.on(
    NewMessage(
        pattern=".*imgur\\.com.*",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def explicit_imgur_clip(event: NewMessage.Event):
    """Set the media chat."""
    await reddit.handle(event, event.message.message, TargetFormat.Mp4)
