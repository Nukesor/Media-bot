import os
import json
import pprint
import youtube_dl
from urllib.request import urlopen, Request

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',

}


def download_media(url):
    """Downloads media from reddit from a given url"""
    info = {'url': url}
    if not url.endswith('.json'):
        url += '.json'
    info = {'json_url': url}
    print(url)
    # Get the json information from reddit
    request = Request(url, headers=headers)
    response = urlopen(request)
    data = response.read().decode("utf-8")
    payload = json.loads(data)

    # Extract the media information from the payload
    info = get_media_info(payload, info)

    # Check if we got some kind of info
    if info is None:
        return None, None

    # Try to download the media using youtube-dl
    # Videos with sound or youtube videos can be eaily downloaded with youtube-dl
    if info['type'] == 'video':
        info, media = get_youtube_dl_media(info)
        if media is not None:
            return info, media

    # Download videos without sound and images
    media = get_media(info)

    return info, media


def get_media_info(payload, info):
    """Get the information of the media from the payload."""
    data = payload[0]['data']['children'][0]['data']
    if 'crosspost_parent_list' in data:
        data = data['crosspost_parent_list'][0]

    info['title'] = data['title']

    # Reddit hosted images
    if data['post_hint'] == 'image':
        info['url'] = data['url']
        info['type'] = 'image'
        info['file_name'] = data['title']
        return info

    # Normal reddit hosted videos
    elif data['post_hint'] == 'hosted:video' and data['domain']:
        video_data = data['media']['reddit_video']
        info['url'] = video_data['fallback_url']
        info['type'] = 'video'
        info['filename'] = 'image'
        info['file_name'] = data['title'] + '.mp4'
        return info

#    # External videos
#    elif data['post_hint'] == 'rich:video' and 'secure_media_embed' in data:
#        return {'url': data['secure_media_embed']['media_domain_url'], 'type': 'video'}

    # Youtube video
    elif data['post_hint'] == 'rich:video' and data['domain'] == 'youtu.be':
        info['url'] = data['url']
        info['type'] = 'video'
        return info

    return None


def get_media(info):
    """Get the actual file by the given info.."""
    if info['type'] in ['image', 'video']:
        request = Request(info['url'], headers=headers)
        response = urlopen(request)
        media = response.read()
        return media


def get_youtube_dl_media(info):
    """Try to download a clip via youtube-dl."""
    print('Trying yd')
    options = {
        'outtmpl': f'/tmp/%(title)s.%(ext)s',
        'quiet': True,
    }
    # Try to download the media with youtube-dl
    try:
        ydl = youtube_dl.YoutubeDL(options)
        yd_info = ydl.extract_info(info['url'])
    except Exception as e:
        print('Failed using yd')
        print(e)
        return info, None

    # Compile file path
    path = f"/tmp/{yd_info['title']}.{yd_info['ext']}"

    with open(path, 'rb') as file:
        media = file.read()

    os.remove(path)

    info['youtube_dl'] = True
    return info, media
