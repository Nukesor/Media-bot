"""Bot management logic."""

import toml
from telethon.events import NewMessage

from mediabot import get_peer_information, log
from mediabot.config import config, config_path
from mediabot.telethon import bot


@bot.on(
    NewMessage(
        pattern="memesplease",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def set_media_chat(event: NewMessage.Event):
    """Set the media chat."""
    try:
        chat_id, _ = get_peer_information(event.message.to_id)
        log(f"Setting media chat: {chat_id}")
        config["bot"]["meme_chat_id"] = chat_id

        with open(config_path, "w") as file_descriptor:
            toml.dump(config, file_descriptor)

        await event.respond(f"Chat id set to {chat_id}")
    except Exception as e:
        log(f"Got exception: {e}")


@bot.on(
    NewMessage(
        pattern="memestop",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def delete_media_chat(event: NewMessage.Event):
    """Delete the current media chat id."""
    try:
        config["bot"]["meme_chat_id"] = ""

        with open(config_path, "w") as file_descriptor:
            toml.dump(config, file_descriptor)

        await event.respond("Media chat unset")
    except Exception as e:
        log(f"Got exception: {e}")
