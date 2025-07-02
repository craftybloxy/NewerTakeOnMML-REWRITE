
CUSTOM HASHABLE DATATYPE FOR A SONG, song_id being the hash
A SONG will now be dictionaries of dict refs

BY DEFAULT ABSOLUTELLY NO AUTOMATIC fixes for when songs aren't a perfect match 

USERS should be asked if two artist account are matching across services, DO NOT LINK PUBLIC ARCHIVES, EITHER OFFICIAL SOURCES OR PERSONAL ARCHIVES
if necessary, do link archives but they have to be CLEARLY seperated from the official sources

THE DATABASE AND USER INPUT WILL NOW BE TREATED AS JUST ANOTHER PLUGIN

service_id_meaning{db:local_database, input:user_input}
user_input might become user_interface or user_cli or just cli

date_added to playlist should be the current time if the service does not remember

when combining, the service_id is changed to the oldest date_added in ref

# TODO
Fix metadata not merging
ERROR tests/Song_test.py - AttributeError: 'dict' object has no attribute 'service_id'

**test_add_metadata_from**

Song_ref object
    artist_id str
    artist_name str
    song_id str
    song_title str
    date_added str
    song_metadata dict {album:value, rating:value, tag:value, ...}

song object
    service_id str
    song_refs dict {service_id:song_ref, service_id:song_ref, service_id:song_ref, ...}

playlist_ref object
    service_id str
    playlist_id str
    playlist_name str
    playlist_metadata dict {description:value, author:value, picture:value, ...}

playlist object
    service_id str
    playlist_refs dict {service_id:playlist_ref, service_id:playlist_ref, service_id:playlist_ref, ...}
    songs list [song, song, song, ...]  #This list is ORDERED


                



### Name -> SongId
[ ] FTS in database

## Name -> InServiceId
[ ] Try to Search using the service APIs
[ ] Try to use a trusted database to link different InServiceIds


# NOTE: Use 404 when data is missing, handle 404 in modules.database oh and don't forget the empty playlists
# Actually Don't, that is a terrible idea

# Data templates

Song(
    service_id="--",
    song_refs={
        "--": {
            "artist_id": "aid--__",
            "artist_name": "ana__",
            "song_id": "sid__",
            "song_title": "sti__",
            "date_added": "2024-03-18",
            "song_metadata": {},
        },
    },
)

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

# outdated


                {
                    "service_id": song_data[0],
                    "artist_id": song_data[1],
                    "input_artist_name": song_data[2],
                    "song_id": song_data[3],
                    "input_song_title": song_data[4],
                    "db_song_id": song_data[5]
                }
