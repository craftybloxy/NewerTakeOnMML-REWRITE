class PlaylistRef:
    def __init__(self, playlist_id, playlist_name, playlist_metadata=dict()):
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name
        self.playlist_metadata = playlist_metadata

    def add(self, other):
        if not isinstance(other, PlaylistRef):
            raise TypeError("Can only add PlaylistRef objects together")
        metadata = {
            **self.playlist_metadata,
            **other.playlist_metadata,
        }
        return PlaylistRef(
            playlist_id=self.playlist_id or other.playlist_id,
            playlist_title=self.playlist_title or other.playlist_title,
            playlist_metadata=metadata,
        )

    def copy(self):
        return PlaylistRef(
            playlist_id=self.playlist_id,
            playlist_title=self.playlist_title,
            playlist_metadata=metadata,
        )

    def __add__(self, other):
        return self.add(other)

    def __dict__(self):
        return {
            "playlist_id": self.playlist_id,
            "playlist_title": self.playlist_title,
            "playlist_metadata": self.playlist_metadata,
        }

    def __repr__(self):
        return str(self.__dict__())
