import os
import json
import pprint
import youtube_dl
from urllib.request import urlopen, Request

from mediabot import log
from mediabot.config import config

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
}


def download_media(url):
    """Downloads media from reddit from a given url"""
    log('\nGet media info from reddit')
    info = {'url': url}
    if not url.endswith('.json'):
        url += '.json'
    info = {'json_url': url}
    # Get the json information from reddit
    log(f'--- Download Json: {url}')
    request = Request(url, headers=headers)
    response = urlopen(request)
    data = response.read().decode("utf-8")
    payload = json.loads(data)

    # Extract the media information from the payload
    try:
        info = get_media_info(payload, info)
    except Exception as e:
        log(f'--- Got exception: {e}')
        raise e

    # Check if we got some kind of info
    if info is None:
        return None, None

    log('--- Got media info:')
    log(f'--- {pprint.pformat(info)}')

    log('Get media:')
    # Try to download the media using youtube-dl
    # Videos with sound or youtube videos can be eaily downloaded with youtube-dl
    if info['type'] == 'video' and info.get('youtube_dl', False):
        log('--- Try youtube-dl')
        info, media = get_youtube_dl_media(info)
        if media is not None:
            return info, media

    log('--- Try direct download')
    # Download videos without sound and images
    media = get_media(info)

    return info, media


def get_media_info(payload, info):
    """Get the information of the media from the payload."""
    data = payload[0]['data']['children'][0]['data']
    if 'crosspost_parent_list' in data:
        data = data['crosspost_parent_list'][0]

    info['title'] = data['title']
    info['youtube_dl'] = False

    # Reddit hosted images
    if data['domain'] == 'i.redd.it':
        log('--- Detected reddit image')
        info['url'] = data['url']
        if info['url'].endswith('.jpg'):
            info['type'] = 'image'
            info['file_name'] = data['title'] + '.jpg'
        elif info['url'].endswith('.png'):
            info['type'] = 'image'
            info['file_name'] = data['title'] + '.png'
        elif info['url'].endswith('.gif'):
            info['type'] = 'gif'
            info['file_name'] = data['title'] + '.gif'
        elif info['url'].endswith('.gifv'):
            info['type'] = 'gif'
            info['file_name'] = data['title'] + '.gifv'
        return info

    # Reddit hosted videos
    elif data['domain'] == 'v.redd.it':
        log('--- Detected reddit video')
        video_data = data['media']['reddit_video']
        info['url'] = video_data['fallback_url']
        info['type'] = 'video'
        info['file_name'] = 'video.mp4'
        info['youtube_dl'] = True
        return info

    # Gfycat videos
    elif data['domain'] == 'gfycat.com':
        log('--- Detected gfycat')
        url = data['secure_media']['oembed']['thumbnail_url']
        url = url.replace('size_restricted.gif', 'mobile.mp4')
        info['url'] = url
        info['type'] = 'video'
        info['file_name'] = 'video.mp4'
        return info

    # Youtube video
    elif data['domain'] == 'youtu.be':
        log('--- Detected youtube')
        info['url'] = data['url']
        info['type'] = 'video'
        info['file_name'] = 'video.mp4'
        info['youtube_dl'] = True
        return info

    # Imgur
    elif data['domain'] == 'i.imgur.com':
        # Gif/gifv
        if data['url'].endswith('.gifv') or data['url'].endswith('.gif'):
            log('--- Detected imgur gif')
            # We replace the .gifv and .gif, since imgur supports mp4 anyway
            url = data['url']
            url = url.replace('gifv', 'mp4')
            url = url.replace('gif', 'mp4')
            info['url'] = url
            info['type'] = 'video'
            info['file_name'] = 'video.mp4'

        # Images
        elif data['url'].endswith('.png'):
            log('--- Detected imgur png')
            info['url'] = data['url']
            info['type'] = 'image'
            info['file_name'] = info['title'] + '.png'
        elif data['url'].endswith('.jpg'):
            log('--- Detected imgur jpg')
            info['url'] = data['url']
            info['type'] = 'image'
            info['file_name'] = info['title'] + '.jpg'

        return info

    log(f'--- Failed to detect media type')
    return None


def get_media(info):
    """Get the actual file by the given info.."""
    log(f"--- Downloading media directly: {info['url']}")
    if info['type'] in ['image', 'video', 'gif', 'gifv']:
        request = Request(info['url'], headers=headers)
        response = urlopen(request)
        media = response.read()
        return media


def get_youtube_dl_media(info):
    """Try to download a clip via youtube-dl."""
    options = {
        'outtmpl': f'/tmp/%(title)s.%(ext)s',
        'quiet': True,
    }
    # Try to download the media with youtube-dl
    log(f"--- Downloading via youtube_dl: {info['url']}")
    try:
        ydl = youtube_dl.YoutubeDL(options)
        yd_info = ydl.extract_info(info['url'])

        # Compile file path
        path = f"/tmp/{yd_info['title']}.{yd_info['ext']}"

        with open(path, 'rb') as file:
            media = file.read()

        os.remove(path)

        log('--- Got media')
        info['youtube_dl'] = True
        return info, media

    except Exception as e:
        log('--- Failed to use youtube-dl')
        print(e)
        return info, None
