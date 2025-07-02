from modules.Playlist import Playlist
from modules.PlaylistRef import PlaylistRef
from modules.Song import Song
from modules.SongRef import SongRef
from rich.pretty import pprint
import pytest

"""
Quick and dirty Playlist template
Playlist(
    service_id="--",
    playlist_refs={
        "--": PlaylistRef(
            playlist_id= "pid--__",
            playlist_name= "pna__",
            playlist_metadata= {},
        ),
    },
   songs=[Song(), Song(), Song()],
)
"""


def test_merge_bridge():
    a1 = Song(
        service_id="youtube",
        song_refs={
            "youtube": SongRef(
                artist_id="aidyoutubea",
                artist_name="naa",
                song_id="sida",
                song_title="tia",
                date_added="2024-03-18",
                song_metadata={},
            ),
            "songcloud": SongRef(
                artist_id="aidsongclouda",
                artist_name="naa",
                song_id="sida",
                song_title="tia",
                date_added="2024-03-18",
                song_metadata={},
            ),
        },
    )

    a2 = Song(
        service_id="spotify",
        song_refs={
            "spotify": SongRef(
                artist_id="aidspotifya",
                artist_name="naa",
                song_id="sida",
                song_title="tia",
                date_added="2024-03-18",
                song_metadata={},
            ),
        },
    )

    a3 = Song(
        service_id="db",
        song_refs={
            "db": SongRef(
                artist_id="aiddba",
                artist_name="naa",
                song_id="sida",
                song_title="tia",
                date_added="2024-03-18",
                song_metadata={},
            ),
            "youtube": SongRef(
                artist_id="aidyoutubea",
                artist_name="naa",
                song_id="sida",
                song_title="tia",
                date_added="2024-03-18",
                song_metadata={},
            ),
            "spotify": SongRef(
                artist_id="aidspotifya",
                artist_name="naa",
                song_id="sida",
                song_title="tia",
                date_added="2024-03-18",
                song_metadata={},
            ),
        },
    )

    myplaylist = Playlist(
        service_id="db",
        playlist_refs={
            "db": PlaylistRef(
                playlist_id= "piddba",
                playlist_name= "pnaa",
                playlist_metadata= {},
            ),
        },
        songs=[],
    )

    myplaylist.update([a1, a2])
    myplaylist.add(a3)
    assert len(myplaylist._songs) == 1


def test_add_metadata_from():
    # Songs that exist in both playlists with shared youtube ref for merging
    j1 = Song(
        service_id="youtube",
        song_refs={
            "youtube": SongRef(
                artist_id="aidyoutubej",
                artist_name="naj",
                song_id="sidj",
                song_title="tij",
                date_added="2024-03-27",
                song_metadata={"duration": 180},
            ),
        },
    )
    j2 = Song(
        service_id="spotify",
        song_refs={
            "spotify": SongRef(
                artist_id="aidspotifyj",
                artist_name="naj",
                song_id="sidj",
                song_title="tij",
                date_added="2024-03-27",
                song_metadata={"genre": "rock", "album": "test_album"},
            ),
        },
    )

    # Songs unique to each playlist
    j3 = Song(
        service_id="spotify",
        song_refs={
            "youtube": SongRef(
                artist_id="aidyoutubej",
                artist_name="naj",
                song_id="sidj",
                song_title="tij",
                date_added="2024-03-27",
                song_metadata={"duration": 180},
            ),
            "spotify": SongRef(
                artist_id="aidspotifyj",
                artist_name="naj",
                song_id="sidj",
                song_title="tij",
                date_added="2024-03-27",
                song_metadata={"genre": "rock", "album": "test_album"},
            ),
        },
    )

    playlist1 = Playlist(
        service_id="youtube",
        playlist_refs={
            "youtube": PlaylistRef(
                playlist_id= "pidyoutubej",
                playlist_name= "pnaj",
                playlist_metadata= {},
            ),
        },
        songs=[j1, j2],
    )

    playlist2 = Playlist(
        service_id="spotify",
        playlist_refs={
            "spotify": PlaylistRef(
                playlist_id= "pidspotifyj",
                playlist_name= "pnaj",
                playlist_metadata= {},
            ),
        },
        songs=[j3],
    )

    # Test the add_metadata_from method
    playlist1.add_metadata_from(playlist2)
    assert "youtube" in playlist1[0].song_refs.keys()
    assert "spotify" in playlist1[0].song_refs.keys()




if __name__ == "__main__":
    test_merge_bridge()
    test_add_metadata_from()
