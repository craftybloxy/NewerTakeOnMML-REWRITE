from datetime import datetime
from rich.pretty import pprint


class SongRef:
    def __init__(
        self,
        artist_id=None,
        artist_name=None,
        song_id=None,
        song_title=None,
        date_added=datetime.today().strftime("%Y-%m-%d"),
        song_metadata=dict(),
    ):
        self.artist_id = artist_id
        self.artist_name = artist_name
        self.song_id = song_id
        self.song_title = song_title
        self.date_added = date_added
        self.song_metadata = song_metadata

    def merge(self, other):
        if not isinstance(other, SongRef):
            raise TypeError("Can only add SongRef objects together")

        metadata = {
            **self.song_metadata,
            **other.song_metadata,
        }

        if self.date_added < other.date_added:
            date = self.date_added
        else:
            date = other.date_added
        return SongRef(
            artist_id=self.artist_id or other.artist_id,
            artist_name=self.artist_name or other.artist_name,
            song_id=self.song_id or other.song_id,
            song_title=self.song_title or other.song_title,
            date_added=date,
            song_metadata=metadata,
        )

    def dictionary(self):
        return {
            "artist_id": self.artist_id,
            "artist_name": self.artist_name,
            "song_id": self.song_id,
            "song_title": self.song_title,
            "date_added": self.date_added,
            "song_metadata": self.song_metadata,
        }
    
    def __repr__(self):
        return str(self.dictionary())
