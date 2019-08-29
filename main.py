#!/bin/python3
"""Telethon related logic."""
import sys
import toml
from telethon import TelegramClient, events, types

from mediabot.config import config
from mediabot.download import download_media

bot = TelegramClient('reddit_media_bot', config['telegram']['app_api_id'], config['telegram']['app_api_hash'])


@bot.on(events.NewMessage(pattern='.*reddit\.com.*'))
async def replace_media_link(event):
    """Set query attributes."""
    try:
        me = await bot.get_me()
        if event.message.from_id != me.id:
            return

        url = event.message.message
        info, media = download_media(url)
        if info is None:
            return

        file_handle = await bot.upload_file(media, file_name=info['file_name'])

        await bot.send_file(event.message.to_id,
                            file=file_handle,
                            caption=info['title'],
                            )
        await event.message.delete()
    except Exception as e:
        pass


bot.start(phone=config['telegram']['phone_number'])
bot.run_until_disconnected()
