import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from modules.cache import cache
from rich.pretty import pprint
from Levenshtein import distance
import re

SERVICE_ID = "spotify"

default_config = {
    "enabled": True,
    "auth_token": "",
}

def init_config(config):
    global _config
    _config = config
    print(_config )

class Plugin:
    def __init__(self):
        ALL_SAVED_PLAYLISTS = True
        load_dotenv("./.env")
        print("logging into spotify..")
        scope = "user-library-read, playlist-read-private, playlist-read-collaborative, playlist-modify-public, playlist-modify-private"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        print("logged into spotify!")

def ping():
    print(SERVICE_ID)


def parse_song_data(track):
    # Get track from the entry

    if not track:
        return None

    artists = track.get("artists")

    if not artists:
        artists = ({"name": None, "id": None},)
    return {
        "service_id": SERVICE_ID,
        "artist_id": artists[0].get("id"),
        "artist_name": artists[0].get("name"),
        "song_id": track.get("id"),
        "song_title": track.get("name"),
    }


@cache
def pull_songs():
    results = []
    raw_data = sp.current_user_saved_tracks(limit=50)
    while raw_data:
        for raw_song in raw_data["items"]:
            song = parse_song_data(raw_song["track"])
            if song:
                results.append(song)
        if raw_data["next"]:
            raw_data = sp.next(raw_data)
        else:
            raw_data = None
    return results


@cache
def pull_playlists():
    # Initialize an empty list for results
    results = []

    # Fetch current user's id
    spotify_user_id = sp.current_user()["id"]
    # Fetch current user's playlists
    raw_data = sp.user_playlists(user=spotify_user_id, limit=50)

    # Iterate through the pages of playlists
    while raw_data:
        for playlist in raw_data["items"]:
            if playlist["owner"]["id"] == spotify_user_id or ALL_SAVED_PLAYLISTS:
                playlist_data = {
                    "service_id": SERVICE_ID,
                    "playlist_id": playlist["id"],
                    "playlist_name": playlist["name"],
                    "songs": [],
                }

                # Get tracks for the playlist, also paginated
                track_data = sp.playlist_tracks(playlist["id"], limit=50)
                while track_data:
                    for item in track_data["items"]:
                        # Use the parse_song_data function to extract and format song data
                        song = parse_song_data(item["track"])
                        if song:
                            playlist_data["songs"].append(song)

                    if track_data["next"]:
                        track_data = sp.next(track_data)
                    else:
                        track_data = None

                results.append(playlist_data)

        # Move to the next page of playlists if available
        if raw_data["next"]:
            raw_data = sp.next(raw_data)
        else:
            raw_data = None

    # Now results contains all playlists with all songs
    return results



def identify_song(song):
    result = None
    clean_title = re.sub(r"[\(\[].*?[\)\]]", "", song["input_song_title"])
    input_artist_name = song.get("input_artist_name")
    if input_artist_name:
        raw_data = sp.search(
            q=f'{song["input_artist_name"]} {clean_title}',
            limit=1,
            type="track",
        )
    else:
        raw_data = sp.search(
            q=clean_title,
            limit=1,
            type="track",
        )

    if not raw_data["tracks"]["items"]:
        song["song_title"] = "None"
        print(f"{clean_title}, not found")
        return None
        # return song

    result = parse_song_data(raw_data["tracks"]["items"][0])

    input_artist_name = song.get("input_artist_name")
    if input_artist_name:
        if not result["artist_name"].lower() == song["input_artist_name"].lower():
            pprint(
                f'{song["input_artist_name"]} =/= {result["artist_name"].lower()} {clean_title}, not found'
            )
            song["song_title"] = "None"
            return None
            # return song
    db_song_id = song.get("db_song_id")
    if db_song_id:
        result["db_song_id"] = song["db_song_id"]

    return result


def songs_from_list(title_list):
    return identify_songs([{"input_song_title": title} for title in title_list])


def push_playlist(playlist):
    pass

