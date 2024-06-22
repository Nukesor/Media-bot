from telethon.events import NewMessage

from mediabot import log
from mediabot.adapters import ytdlp
from mediabot.media_info import Adapter, Info, Source, TargetFormat
from mediabot.telethon.files import handle_file_backup, handle_file_upload


async def handle(event: NewMessage.Event, target_format: TargetFormat):
    text = event.message.message
    url = text.split(" ")[1]

    # The title info is set lateron by yt-dlp
    info = Info(url, "", Source.Youtube, Adapter.Ytdlp, target_format)

    try:
        info, media = ytdlp.download_media(info)
        await handle_file_backup(event, info, media)
        await handle_file_upload(event, info, media)
    except Exception as e:
        log(f"Failed to handle youtube link. Got exception: {e}")
    pass
