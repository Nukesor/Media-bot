"""Bot management logic."""
import toml
from telethon import events

from mediabot.telethon import bot
from mediabot.config import config, config_path
from mediabot import log, get_peer_information


@bot.on(events.NewMessage(pattern="memesplease"))
async def set_media_chat(event):
    """Set the media chat."""
    try:
        me = await bot.get_me()
        if event.message.from_id != me.id:
            return

        chat_id, peer_type = get_peer_information(event.message.to_id)
        log(f"Setting media chat: {chat_id}")
        config["bot"]["meme_chat_id"] = chat_id

        with open(config_path, "w") as file_descriptor:
            toml.dump(config, file_descriptor)

        await event.respond(f"Chat id set to {chat_id}")
    except Exception as e:
        log(f"Got exception: {e}")


@bot.on(events.NewMessage(pattern="memestop"))
async def delete_media_chat(event):
    """Delete the current media chat id."""
    try:
        me = await bot.get_me()
        if event.message.from_id != me.id:
            return

        config["bot"]["meme_chat_id"] = ""

        with open(config_path, "w") as file_descriptor:
            toml.dump(config, file_descriptor)

        await event.respond(f"Media chat unset")
    except Exception as e:
        log(f"Got exception: {e}")


@bot.on(events.NewMessage(pattern="chat_id"))
async def print_chat_id(event):
    """Print the current chat id and type for debugging."""
    try:
        me = await bot.get_me()
        if event.message.from_id != me.id:
            return

        chat_id, peer_type = get_peer_information(event.message.to_id)
        message = f"Chat type: {peer_type}, chat id: {chat_id}"

        await event.respond(message)
    except Exception as e:
        log(f"Got exception: {e}")
