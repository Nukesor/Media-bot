import os

from telethon import types
from telethon.events import NewMessage

from mediabot import get_peer_information, get_sender_information, log
from mediabot.config import config
from mediabot.media_info import Info
from mediabot.telethon import bot


async def handle_file_upload(event: NewMessage.Event, info: Info, media: bytes):
    """Telethon file upload related logic."""
    log("Handle telethon stuff:")
    log(f"--- Upload: {info.title}")
    file_handle = await bot.upload_file(media, file_name=info.file_name())

    me = await bot.get_me()
    from_id, _ = get_sender_information(event)

    # Allow to have a different caption than file title
    if info.caption is not None:
        caption = info.caption
    else:
        caption = info.title

    # Send the file to the chat and replace the message
    # if the message was send by yourself
    if from_id == me.id:
        log("--- Send to original chat")
        await bot.send_file(
            event.message.to_id,
            file=file_handle,
            caption=caption,
        )

        log("--- Delete original message")
        await event.message.delete()

    # Send the file to a meme chat if it's specified
    chat_id, _ = get_peer_information(event.message.to_id)
    meme_chat_id = config["bot"]["meme_chat_id"]

    if meme_chat_id != "" and meme_chat_id != chat_id:
        log("--- Send media to meme chat")
        meme_chat = await bot.get_entity(types.PeerChat(meme_chat_id))
        await bot.send_file(
            meme_chat,
            file=file_handle,
            caption=caption,
        )


async def handle_file_backup(event: NewMessage.Event, info: Info, media: bytes):
    """Backup the file to the disk, if config says so."""
    if config["bot"]["backup"]:
        log("Backing up media to disk")
        await backup_file(event, info, media)


async def backup_file(event: NewMessage.Event, info: Info, media: bytes):
    """Backup the media to a file."""
    # Compile file name
    file_name = info.file_name_with_date()

    log(f"--- File name: {file_name}")
    from_id, _ = get_sender_information(event)

    # Get username
    user = await bot.get_entity(from_id)
    username = get_username(user)

    # Compile path
    base_path = os.path.expanduser(config["bot"]["backup_path"])
    dir_path = os.path.join(base_path, username)
    file_path = os.path.join(dir_path, file_name)
    log(f"--- Path : {file_path}")
    os.makedirs(dir_path, mode=0o755, exist_ok=True)

    # Write to disk
    with open(file_path, "wb") as media_file:
        media_file.write(media)
    log("--- Saved to disk!")


def get_username(user):
    """Get a username from a user.

    Try to get any name first, fallback to id.
    """
    if user.username:
        return user.username
    elif user.first_name:
        return user.first_name
    elif user.last_name:
        return user.last_name
    else:
        return str(user.id)
