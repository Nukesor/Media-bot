"""Handle file backup logic."""
import os
from datetime import date
from telethon import types

from mediabot import log
from mediabot.config import config


async def backup_file(bot, from_id, info, media):
    """Backup the media to a file."""
    # Compile file name
    today = date.today().isoformat()
    title = info['title']
    extension = info['type']
    file_name = f"{today}_{title}.{extension}"

    log(f"--- File name: {file_name}")
    # Get username
    user = await bot.get_entity(types.PeerUser(from_id))
    username = get_username(user)
    log(f"--- Username: {username}")

    # Compile path
    dir_path = os.path.join(config['bot']['backup_path'], username)
    file_path = os.path.join(dir_path, file_name)
    log(f"--- Username: {file_path}")
    os.makedirs(dir_path, mode=0o755, exist_ok=True)

    # Write to disk
    with open(file_path, 'wb') as media_file:
        media_file.write(media)
    log(f"--- Saved to disk!")


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
