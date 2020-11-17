"""Bot management logic."""
import toml
from telethon import events

from mediabot.telethon import bot
from mediabot.config import config, config_path
from mediabot import log, get_peer_information


@bot.on(
    events.NewMessage(
        pattern="memesplease",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def set_media_chat(event):
    """Set the media chat."""
    try:
        chat_id, peer_type = get_peer_information(event.message.to_id)
        log(f"Setting media chat: {chat_id}")
        config["bot"]["meme_chat_id"] = chat_id

        with open(config_path, "w") as file_descriptor:
            toml.dump(config, file_descriptor)

        await event.respond(f"Chat id set to {chat_id}")
    except Exception as e:
        log(f"Got exception: {e}")


@bot.on(
    events.NewMessage(
        pattern="memestop",
        outgoing=True,
        forwards=False,
        from_users=config["bot"]["admin"],
    )
)
async def delete_media_chat(event):
    """Delete the current media chat id."""
    try:
        config["bot"]["meme_chat_id"] = ""

        with open(config_path, "w") as file_descriptor:
            toml.dump(config, file_descriptor)

        await event.respond(f"Media chat unset")
    except Exception as e:
        log(f"Got exception: {e}")
