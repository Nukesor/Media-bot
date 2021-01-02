from telethon import types

from mediabot.config import config


def log(message):
    """Log message if logging is enabled."""
    if config["logging"]["debug"]:
        print(message)


def get_sender_information(event):
    """Get the peer information of a message's sender."""
    # Telegram doesn't always send `from_id` :<<<
    # This happens if, for instance, links are sent with link preview.
    from_id = event.message.from_id
    if from_id is None:
        from_id = event.message.peer_id

    return get_peer_information(from_id)


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
