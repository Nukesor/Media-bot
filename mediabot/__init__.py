from telethon import types

from mediabot.config import config


def log(message):
    """Log message if logging is enabled."""
    if config["logging"]["debug"]:
        print(message)


def get_peer_information(peer):
    """Get the id depending on the chat type."""
    if isinstance(peer, types.PeerUser):
        return peer.user_id, "user"
    elif isinstance(peer, types.PeerChat):
        return peer.chat_id, "peer"
    elif isinstance(peer, types.PeerChannel):
        return peer.channel_id, "channel"
    else:
        raise Exception("Unknown chat type")
