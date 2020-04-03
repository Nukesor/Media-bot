"""Telethon bot instance creation."""
from telethon import TelegramClient

from mediabot.config import config


bot = TelegramClient(
    "reddit_media_bot",
    config["telegram"]["app_api_id"],
    config["telegram"]["app_api_hash"],
)


# Reexport for easy bot initialization
from .management import *
from .media import *
