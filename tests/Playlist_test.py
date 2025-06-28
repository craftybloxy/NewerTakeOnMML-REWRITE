from modules.Playlist import Playlist
from modules.Song import Song
import pytest

"""
Quick and dirty Playlist template
Playlist(
    service_id="--",
    playlist_refs={
        "--": {
            "playlist_id": "pid--__",
            "playlist_name": "pna__",
            "playlist_metadata": {},
        },
    },
   songs=[Song(), Song(), Song()],
)
"""


def test_merge_bridge():
    a1 = Song(
        service_id="youtube",
        song_refs={
            "youtube": {
                "artist_id": "aidyoutubea",
                "artist_name": "naa",
                "song_id": "sida",
                "song_title": "tia",
                "date_added": "2024-03-18",
                "song_metadata": {},
            },
            "songcloud": {
                "artist_id": "aidsongclouda",
                "artist_name": "naa",
                "song_id": "sida",
                "song_title": "tia",
                "date_added": "2024-03-18",
                "song_metadata": {},
            },
        },
    )

    a2 = Song(
        service_id="spotify",
        song_refs={
            "spotify": {
                "artist_id": "aidspotifya",
                "artist_name": "naa",
                "song_id": "sida",
                "song_title": "tia",
                "date_added": "2024-03-18",
                "song_metadata": {},
            },
        },
    )

    a3 = Song(
        service_id="db",
        song_refs={
            "db": {
                "artist_id": "aiddba",
                "artist_name": "naa",
                "song_id": "sida",
                "song_title": "tia",
                "date_added": "2024-03-18",
                "song_metadata": {},
            },
            "youtube": {
                "artist_id": "aidyoutubea",
                "artist_name": "naa",
                "song_id": "sida",
                "song_title": "tia",
                "date_added": "2024-03-18",
                "song_metadata": {},
            },
            "spotify": {
                "artist_id": "aidspotifya",
                "artist_name": "naa",
                "song_id": "sida",
                "song_title": "tia",
                "date_added": "2024-03-18",
                "song_metadata": {},
            },
        },
    )

    myplaylist = Playlist(
        service_id="db",
        playlist_refs={
            "db": {
                "playlist_id": "piddba",
                "playlist_name": "pnaa",
                "playlist_metadata": {},
            },
        },
        songs=[],
    )

    myplaylist.update([a1, a2])
    myplaylist.add(a3)
    assert len(myplaylist._songs) == 1
