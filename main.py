#!/bin/python3
"""Entry script."""

from mediabot.telethon import bot
from mediabot.config import config


bot.start(phone=config['telegram']['phone_number'])
bot.run_until_disconnected()
