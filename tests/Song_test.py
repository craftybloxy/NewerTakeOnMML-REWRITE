from modules.Song import Song
from modules.SongRef import SongRef

"""
quick and dirty Song template
Song(
    service_id="--",
    song_refs={
        "--": SongRef (
            artist_id= "aid--__",
            artist_name= "na__",
            song_id= "sid__",
            song_title= "ti__",
            date_added= "2024-03-18",
            song_metadata ={},
        ),
    },
)
"""


one1 = Song(
    service_id="youtube",
    song_refs={
        "youtube": SongRef(
            artist_id="aidyoutube1",
            artist_name="na1",
            song_id="sid1",
            song_title="ti1",
            date_added="2024-03-18",
            song_metadata={},
        ),
    },
)
one2 = Song(
    service_id="spotify",
    song_refs={
        "spotify": SongRef(
            artist_id="aidspotify1",
            artist_name="na1",
            song_id="sid1",
            song_title="ti1",
            date_added="2023-03-18",
            song_metadata={},
        ),
        "youtube": SongRef(
            artist_id="aidyoutube1",
            artist_name="na1",
            song_id="sid1",
            song_title="ti1",
            date_added="2024-03-18",
            song_metadata={},
        ),
    },
)

two1 = Song(
    service_id="youtube",
    song_refs={
        "youtube": SongRef(
            artist_id="aidyoutube2",
            artist_name="na2",
            song_id="sid2",
            song_title="ti2",
            date_added="2024-03-18",
            song_metadata={},
        ),
    },
)


def test_equality():
    assert one1 == one2


def test_inequality():
    assert not one1 == two1


def test_oldest_id_change():
    result = one1 + one2
    assert result.service_id == "spotify"

if __name__ == "__main__":
    test_equality()
    test_inequality()
    test_oldest_id_change()