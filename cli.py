#!/bin/python3
import sys
from download import download_media


def main():
    """Commandline entry point."""
    url = sys.argv[1]
    info, media = download_media(url)

    print(info)
    print(media)

    with open('test', 'wb') as f:
        f.write(media)


main()
