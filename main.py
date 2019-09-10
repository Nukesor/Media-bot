#!/bin/python3
"""Telethon related logic."""
import sys
import toml
from telethon import TelegramClient, events, types

from mediabot import log, get_peer_information
from mediabot.config import config, config_path
from mediabot.download import download_media

bot = TelegramClient('reddit_media_bot', config['telegram']['app_api_id'], config['telegram']['app_api_hash'])


@bot.on(events.NewMessage(pattern='.*reddit\.com.*'))
async def replace_media_link(event):
    """Replace a reddit link with the actual media of the reddit link."""
    try:
        url = event.message.message
        info, media = download_media(url)
        if info is None or media is None:
            return

        log("Got info and media, handling telethon stuff:")
        log(f"--- Uploading: {info['title']}, {info['file_name']}")
        file_handle = await bot.upload_file(media, file_name=info['file_name'])

        log("--- Sending")
        me = await bot.get_me()
        if event.message.from_id == me.id:
            log("--- Sending to chat")
            await bot.send_file(
                event.message.to_id,
                file=file_handle,
                caption=info['title'],
            )

            log("--- Deleting old message")
            await event.message.delete()

        chat_id, chat_type = get_peer_information(event.message.to_id)
        meme_chat_id = config['telegram']['meme_chat_id']
        if meme_chat_id != '' and meme_chat_id != chat_id:
            log("--- Sending to meme chat")
            await bot.send_file(
                config['telegram']['meme_chat_id'],
                file=file_handle,
                caption=info['title'],
            )

    except Exception as e:
        log(f"Got exception: {e}")
        pass


@bot.on(events.NewMessage(pattern='memesplease'))
async def set_media_chat(event):
    """Set the media chat."""
    try:
        me = await bot.get_me()
        if event.message.from_id != me.id:
            return

        chat_id, peer_type = get_peer_information(event.message.to_id)
        log(f"Setting media chat: {chat_id}")
        config['telegram']['meme_chat_id'] = chat_id

        with open(config_path, "w") as file_descriptor:
            toml.dump(config, file_descriptor)

        await event.respond(f'Chat id set to {chat_id}')
    except Exception as e:
        log(f"Got exception: {e}")


@bot.on(events.NewMessage(pattern='memestop'))
async def delete_media_chat(event):
    """Delete the current media chat id."""
    try:
        me = await bot.get_me()
        if event.message.from_id != me.id:
            return

        config['telegram']['meme_chat_id'] = ''

        with open(config_path, "w") as file_descriptor:
            toml.dump(config, file_descriptor)

        await event.respond(f'Chat id set to {chat_id}')
    except Exception as e:
        log(f"Got exception: {e}")

bot.start(phone=config['telegram']['phone_number'])
bot.run_until_disconnected()
