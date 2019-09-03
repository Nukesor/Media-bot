from mediabot.config import config


def log(message):
    """Log message if logging is enabled."""
    if config['logging']['debug']:
        print(message)
