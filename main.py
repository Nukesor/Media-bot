#!/bin/env python
"""Start the bot."""
import typer
import pprint

from mediabot.telethon import bot
from mediabot.config import config


cli = typer.Typer()


@cli.command()
def print_config():
    """Print the current config."""
    pprint.pprint(config)


@cli.command()
def run():
    """Actually start the bot."""
    print("Starting up mediabot.")
    bot.start(phone=config["telegram"]["phone_number"])
    bot.run_until_disconnected()


if __name__ == "__main__":
    cli()
