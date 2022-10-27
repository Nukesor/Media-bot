# Reddit media bot

[![MIT Licence](https://img.shields.io/badge/license-MIT-success.svg)](https://github.com/Nukesor/reddit-media-bot/blob/master/LICENSE.md)

A telegram user bot which replaces reddit links in messages with the actual media file from the reddit post (video, gif, image).

For instance, when sending a link to a reddit post with a video, the bot will download the video, upload it to telegram, and replace the reddit link message with the actual video file.

## Features

- Backup memes to a folder on your server
- Support for messages shared via BaconReader
- Support for other meme source links:
  - Imgur
  - Youtube
  - Gfycat
  - Giphy

## Installation and Starting

**This bot is developed for Linux.**

Dependencies:

- `poetry` to manage and install dependencies.

1. Clone the repository:

    ```sh
    git clone git@github.com:nukesor/reddit-media-bot redditbot && cd redditbot
    ```

1. Execute `just setup` to install all dependencies.
1. Run `just run` to create a default config `~/.config/archivebot.toml`
1. Adjust the configuration
1. Start the bot via `just run`

## Example URLs

The following are example urls that can be used to debug all possible medias.

### Reddit Web Links

#### v.reddit.com

- https://www.reddit.com/r/EscapefromTarkov/comments/dub8gq/when_tarkov_really_doesnt_want_you_to_extract.json

#### i.reddit.com

- https://www.reddit.com/r/me_irl/comments/dubdhm/me_irl.json

#### imgur.com

- http://reddit.com/r/gifs/comments/dtl50i/rip_camera/

#### i.imgur.com

- https://www.reddit.com/r/aww/comments/dub2pb/gimme_a_turn/

#### gyfcat.com

- https://www.reddit.com/r/Unexpected/comments/ducyp3/excuse_me_i_believe_thats_illegal/

#### youtube.com

- https://www.reddit.com/r/videos/comments/ducbu2/wendys_training_video_is_what_i_wish_we_were/

#### media.giphy.com

- https://www.reddit.com/r/gifs/comments/du4jow/sleeping_kitten/

### Direct URLs

#### i.reddit.com

- https://i.redd.it/y7tytlqn1vx31.jpg

#### i.imgur.com

- https://i.imgur.com/VQ4ScOr.gifv

#### imgur.com

- https://imgur.com/A5FfVJU.gifv

#### gyfcat.com 

- https://gfycat.com/scientificinfatuatedbittern

#### youtube.com

- https://www.youtube.com/watch?v=_ZXeFPpPJeI

#### media.giphy.com

- https://media.giphy.com/media/WUyDjgT3I4bSbPFSIU/giphy.gif
- https://media2.giphy.com/media/sNgoEmN4AadgY/giphy.gif?cid=4d1e4f292b84f038e60cc3c6a9fde741f2da2e365cba1adc&rid=giphy.gif
