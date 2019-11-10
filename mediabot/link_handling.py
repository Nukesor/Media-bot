"""Media url link handling logic."""
from mediabot import log


def info_from_ireddit(info, url):
    """Populate info object with info from i.redd.it url."""
    log('--- Detected reddit image')
    info.url = url
    if info.url.endswith('.jpg'):
        info.type = 'jpg'
    elif info.url.endswith('.png'):
        info.type = 'png'
    elif info.url.endswith('.gif'):
        info.type = 'gif'
    elif info.url.endswith('.gifv'):
        info.type = 'gifv'


def info_from_vreddit(info, url):
    """Populate info object with info from v.redd.it url."""
    log('--- Detected reddit video')
    info.url = url
    info.type = 'mp4'
    info.youtube_dl = True

    return info


def info_from_gyfcat(info, url):
    """Populate info object with info from gyfcat.com url."""
    log('--- Detected gfycat')
    url = url.replace('size_restricted.gif', 'mobile.mp4')
    info.url = url
    info.type = 'mp4'
    return info


def info_from_giphy(info, url):
    """Populate info object with info from *.giphy.com url."""
    log('--- Detected giphy')
    url = url.replace('media.giphy.com', 'i.giphy.com')
    url = url.replace('media1.giphy.com', 'i.giphy.com')
    url = url.replace('media2.giphy.com', 'i.giphy.com')
    url = url.replace('giphy.gif', 'giphy.mp4')
    info.url = url
    info.type = 'mp4'
    return info


def info_from_youtube(info, url):
    """Populate info object with info from youtube.com url."""
    log('--- Detected youtube')
    info.url = url
    info.type = 'mp4'
    info.youtube_dl = True
    return info


def info_from_imgur(info, url):
    """Populate info object with info from *.imgur.com url."""
    # Gif/gifv
    if url.endswith('.gifv') or url.endswith('.gif'):
        log('--- Detected imgur gif')
        # We replace the .gifv and .gif, since imgur supports mp4 anyway
        url = url.replace('gifv', 'mp4')
        url = url.replace('gif', 'mp4')
        info.url = url
        info.type = 'mp4'

    # Images
    elif url.endswith('.png'):
        log('--- Detected imgur png')
        info.url = url
        info.type = 'png'
    elif url.endswith('.jpg'):
        log('--- Detected imgur jpg')
        info.url = url
        info.type = 'jpg'

    return info

