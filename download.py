import json
import pprint
from urllib.request import urlopen, Request

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',

}


def download_media(url):
    """Downloads media from reddit from a given url"""
    if not url.endswith('.json'):
        url += '.json'

    # Get the json information from reddit
    request = Request(url, headers=headers)
    response = urlopen(request)
    data = response.read().decode("utf-8")
    payload = json.loads(data)

    # Extract the media information from the payload
    info = get_media_info(payload)
    media = get_media(info)

    return info, media


def get_media_info(payload):
    """Get the information of the media from the payload."""
    data = payload[0]['data']['children'][0]['data']

    # Reddit hosted images
    if data['post_hint'] == 'image':
        return {'url': data['url'], 'type': 'image'}

    # Normal reddit hosted videos
    elif data['post_hint'] == 'hosted:video' and data['domain']:
        video_data = data['media']['reddit_video']
        return {'url': video_data['fallback_url'], 'type': 'video'}

#    # External videos
#    elif data['post_hint'] == 'rich:video' and 'secure_media_embed' in data:
#        return {'url': data['secure_media_embed']['media_domain_url'], 'type': 'video'}

    # Youtube videos
    elif data['post_hint'] == 'rich:video' and data['domain'] == 'youtu.be':
        return {'url': data['url'], 'type': 'youtube'}


def get_media(info):
    """Get the actual file by the given info.."""
    if info['type'] == 'image':
        request = Request(info['url'], headers=headers)
        response = urlopen(request)
        media = response.read()
        return media
