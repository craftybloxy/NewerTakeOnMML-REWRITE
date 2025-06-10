from modules.Song import Song
from modules.SongSet import SongSet
from rich.pretty import pprint

another_mistake = Song(
    {
        "song_id": 1,
        "song_title": "Another Mistake",
        "song_refs": {
            "youtube": {
                "artist_id": "yonakgor",
                "artist_name": "Yonakgor",
                "song_id": "s1",
                "song_title": "Another Mistake",
            },
            "spotify": {
                "artist_id": "yonakgor",
                "artist_name": "Yonakgor",
                "song_id": "s1",
                "song_title": "Another Mistake",
            },
        },
    }
)

another_mistake_alt = Song(
    {
        "song_refs": {
            "soundcloud": {
                "artist_id": "yonakgor",
                "artist_name": "Yonakgor",
                "song_id": "s1",
                "song_title": "Another Mistake",
            },
            "spotify": {
                "artist_id": "yonakgor",
                "artist_name": "Yonakgor",
                "song_id": "s1",
                "song_title": "Another Mistake",
            },
        }
    }
)

nothing = Song(
    {
        "song_id": 1,
        "song_title": "Nothing",
        "song_refs": {
            "spotify": {
                "artist_id": "kennyoung",
                "artist_name": "Kennyoung",
                "song_id": "s3",
                "song_title": "Nothing",
            },
            "youtube": {
                "artist_id": "kennyoung",
                "artist_name": "Kennyoung",
                "song_id": "s3",
                "song_title": "Nothing",
            },
        },
    }
)

nothing_alt = Song(
    {
        "song_id": 3,
        "song_title": "Nothing",
        "song_refs": {
            "spotify": {
                "artist_id": "kennyoung",
                "artist_name": "Kennyoung",
                "song_id": "s1",
                "song_title": "Nothing",
            },
            "deezer": {
                "artist_id": "kennyoung",
                "artist_name": "Kennyoung",
                "song_id": "s2",
                "song_title": "Nothing",
            },
        },
    }
)

# Test set operations
song_set = SongSet([another_mistake, another_mistake_alt, nothing, nothing_alt])
print(song_set)
# Test equality
print(f"another_mistake == nothing: {another_mistake == nothing}")
print(
    f"another_mistake == another_mistake_alt: {another_mistake == another_mistake_alt}"
)
print(f"another_mistake_alt == nothing_alt: {another_mistake_alt == nothing_alt}")
# Test ref merging
merged_song = another_mistake + another_mistake_alt
print("Merged song:")
pprint(merged_song.raw())
