
CUSTOM HASHABLE DATATYPE FOR A SONG, song_id being the hash
A SONG will now be dictionaries of dict refs

BY DEFAULT ABSOLUTELLY NO AUTOMATIC fixes for when songs aren't a perfect match 

USERS should be asked if two artist account are matching across services, DO NOT LINK PUBLIC ARCHIVES, EITHER OFFICIAL SOURCES OR PERSONAL ARCHIVES
if necessary, do link archives but they have to be CLEARLY seperated from the official sources


service_id{db:local_database, input:user_input}

song_ref dict   # service_id -> db for storing local db_id
    service_id str
    artist_id str
    artist_name str
    song_id str
    song_title str

song object
    service_id str
    song_refs list [song_ref, song_ref, song_ref, ...]

playlist_ref dict   # service_id -> db for storing local db_id
    service_id str
    playlist_id str
    playlist_name str

playlist object
    service_id str
    playlist_refs list [playlist_ref, playlist_ref, ...]
    songs list [song, song, song, ...]


                



### Name -> SongId
[ ] FTS in database

## Name -> InServiceId
[ ] Try to Search using the service APIs
[ ] Try to use a trusted database to link different InServiceIds


#
# NOTE: Use 404 when data is missing, handle 404 in modules.database oh and don't forget the empty playlists
#

# Data templates

        {
            "service_id": "spotify",
            "artist_id": "404",
            "artist_name": "John Doe",
            "song_id": "404",
            "song_title": "Amazing Journey",
        }

        {
            "service_id": "spotify",
            "playlist_id": "playlist101_spotify_id",
            "playlist_name": "Morning Vibes",
            "db_playlist_id": None,  
            "songs": [
                {
                    "service_id": "spotify",
                    "artist_id": "artist100_spotify_id",
                    "artist_name": "John Doe",
                    "song_id": "song100_spotify_id",
                    "song_title": "Amazing Journey",
                },
            ]
        }
# Unindentified


                {
                    "service_id": song_data[0],
                    "artist_id": song_data[1],
                    "input_artist_name": song_data[2],
                    "song_id": song_data[3],
                    "input_song_title": song_data[4],
                    "db_song_id": song_data[5]
                }