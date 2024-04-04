from datetime import date
from enum import Enum


class Adapter(Enum):
    """Defines which adapter should be used for downloading media."""

    Ytdlp = 0


class Source(Enum):
    """Defines from which the media is downloaded from."""

    Youtube = 0


class TargetFormat(Enum):
    """Defines in which format the media should be exported."""

    Mp3 = 0
    Mp4 = 1
    Webm = 2


class Info:
    """Class representing information about a requested media file."""

    url: str
    title: str
    caption: str | None = None
    source: Source
    adapter: Adapter
    target_format: TargetFormat

    def __init__(self, url, title, source, adapter, target_format):
        self.url = url
        self.title = title
        self.source = source
        self.adapter = adapter
        self.target_format = target_format

    def file_name(self):
        return f"{self.title}.{self.target_format.name.lower()}"

    def file_name_with_date(self):
        today = date.today().isoformat()
        return f"{today}_{self.file_name()}"

    def __repr__(self):
        return (
            f"\n    Title: {self.title}\n"
            + f"    Caption: {self.caption}\n"
            + f"    Source: {self.source.name} ({self.url})\n"
            + f"    Adapter: {self.adapter.name}\n"
            + f"    File: ({self.target_format.name}) {self.file_name()}\n"
        )
