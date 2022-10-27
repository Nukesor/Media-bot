"""Download and message replace logic."""

import requests
from telethon import events

from mediabot import log
from mediabot.download import Info, download_media, handle_reddit_web_url, headers
from mediabot.link_handling import (
    info_from_gfycat,
    info_from_giphy,
    info_from_imgur,
    info_from_ireddit,
)
from mediabot.telethon import bot
from mediabot.telethon.files import handle_file_backup, handle_file_upload


@bot.on(events.NewMessage(pattern=".*reddit\.com.*"))
async def replace_reddit_post_link(event):
    """Replace a reddit link with the actual media of the reddit link."""
    try:
        url = event.message.message
        info, media = handle_reddit_web_url(url)
        if info is None or media is None:
            return
        await handle_file_backup(event, info, media)
        await handle_file_upload(event, info, media)

    except Exception as e:
        log(f"Got exception: {e}")


@bot.on(events.NewMessage(pattern="(?s).*v\.redd\.it.*"))
async def replace_vreddit_link(event):
    """Handle v.redd.it links."""
    text = event.message.message
    # Remove all empty lines.
    splitted = list(filter(lambda line: line.strip() != "", text.split("\n")))

    if len(splitted) == 1:
        url = splitted[0]
    elif len(splitted) == 2:
        url = splitted[1]
    else:
        return

    response = requests.get(url, headers=headers, allow_redirects=False)
    url = response.headers["Location"]
    response = requests.get(url, headers=headers, allow_redirects=False)
    url = response.headers["Location"]

    try:
        info, media = handle_reddit_web_url(url)
        if info is None or media is None:
            return
        await handle_file_backup(event, info, media)
        await handle_file_upload(event, info, media)

    except Exception as e:
        log(f"Got exception: {e}")


@bot.on(events.NewMessage(pattern="(?s).*i\.redd\.it.*"))
async def replace_ireddit_link(event):
    """Handle i.redd.it links."""
    await download_direct_link(event, info_from_ireddit)


@bot.on(events.NewMessage(pattern="(?s).*imgur\.com.*"))
async def replace_imgur_link(event):
    """Handle imgur links."""
    await download_direct_link(event, info_from_imgur)


@bot.on(events.NewMessage(pattern="(?s).*giphy\.com.*"))
async def replace_giphy_link(event):
    """Handle giphy links."""
    await download_direct_link(event, info_from_giphy)


@bot.on(events.NewMessage(pattern="(?s).*gfycat\.com.*"))
async def replace_gfycat_link(event):
    """Handle gfycat links."""
    await download_direct_link(event, info_from_gfycat)


async def download_direct_link(event, function):
    """Generic download class for forwarded messages."""
    try:
        text = event.message.message
        info = Info()

        log(f"Got link: {text}")
        splitted = text.split("\n")
        if len(splitted) == 1:
            function(info, splitted[0])
            info.title = None
        elif len(splitted) == 2:
            info.title = splitted[0]
            function(info, splitted[1])
        elif len(splitted) > 2:
            return

        info, media = download_media(info)
        await handle_file_backup(event, info, media)
        await handle_file_upload(event, info, media)
    except Exception as e:
        log(f"Got exception: {e}")
        raise e
