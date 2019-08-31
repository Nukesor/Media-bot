# Reddit media bot

[![MIT Licence](https://img.shields.io/badge/license-MIT-success.svg)](https://github.com/Nukesor/reddit-media-bot/blob/master/LICENSE.md)
[![Paypal](https://github.com/Nukesor/images/blob/master/paypal-donate-blue.svg)](https://www.paypal.me/arnebeer/)
[![Patreon](https://github.com/Nukesor/images/blob/master/patreon-donate-blue.svg)](https://www.patreon.com/nukesor)

A telegram user bot which replaces reddit links in messages with the actual media file from the reddit post ( (video, gif, image).

For instance, when sending a link to a reddit post with a video, the bot will download the video, upload it to telegram, and replace the reddit link message with the actual video file.


## Installation and Starting:
**This bot is developed for Linux.** 

Dependencies: 
- `poetry` to manage and install dependencies.

1. Clone the repository:

        % git clone git@github.com:nukesor/reddit-media-bot redditbot && cd redditbot

2. Execute `poetry install` to install all dependencies.
3. Start the bot once with `poetry run python3 main.py` and adjust all necessary values at `~/.config/pollbot.toml`.
4. Run `poetry run initdb.py` to initialize the database.
5. Start the bot `poetry run python3 main.py`
