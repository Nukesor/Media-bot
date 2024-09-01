from telethon.events import NewMessage

from mediabot.config import config
from mediabot.handlers import reddit
from mediabot.helper import url_from_text
from mediabot.media_info import TargetFormat
from mediabot.telethon import bot


@bot.on(
    NewMessage(
        pattern="(?s)(.*reddit\\.com.*|.*v\\.redd\\.it.*)",
        outgoing=True,
        from_users=config["bot"]["admin"],
    )
)
async def reddit_link(event: NewMessage.Event):
    """Set the media chat."""
    link = url_from_text(event.message.message)
    if link is not None:
        await reddit.handle(event, link, TargetFormat.Mp4)


@bot.on(
    NewMessage(
        pattern="\\\\r",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def explicit_reddit_link(event: NewMessage.Event):
    """Handle an explicit link

    The message should have the format `\r https://somelink.com`
    ."""
    text = event.message.message
    url = text.split(" ")[1]
    await reddit.handle(event, url, TargetFormat.Mp4)
