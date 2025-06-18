import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from modules.cache import cache
from rich.pretty import pprint
from Levenshtein import distance
import re

SERVICE_ID = "spotify"

default_settings = {
    "enabled": True,
    "auth_token": "",
}

class Plugin:
    def __init__(self):
        self.ALL_SAVED_PLAYLISTS = True
        load_dotenv("./.env")
        print("logging into spotify..")
        scope = "user-library-read, playlist-read-private, playlist-read-collaborative, playlist-modify-public, playlist-modify-private"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        print("logged into spotify!")

    def ping(self):
        print(SERVICE_ID)

    def parse_song_data(self, track):
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
    def pull_songs(self):
        results = []
        raw_data = self.sp.current_user_saved_tracks(limit=50)
        while raw_data:
            for raw_song in raw_data["items"]:
                song = self.parse_song_data(raw_song["track"])
                if song:
                    results.append(song)
            if raw_data["next"]:
                raw_data = self.sp.next(raw_data)
            else:
                raw_data = None
        return results

    @cache
    def pull_playlists(self):
        results = []
        spotify_user_id = self.sp.current_user()["id"]
        raw_data = self.sp.user_playlists(user=spotify_user_id, limit=50)

        while raw_data:
            for playlist in raw_data["items"]:
                if playlist["owner"]["id"] == spotify_user_id or self.ALL_SAVED_PLAYLISTS:
                    playlist_data = {
                        "service_id": SERVICE_ID,
                        "playlist_id": playlist["id"],
                        "playlist_name": playlist["name"],
                        "songs": [],
                    }

                    track_data = self.sp.playlist_tracks(playlist["id"], limit=50)
                    while track_data:
                        for item in track_data["items"]:
                            song = self.parse_song_data(item["track"])
                            if song:
                                playlist_data["songs"].append(song)

                        if track_data["next"]:
                            track_data = self.sp.next(track_data)
                        else:
                            track_data = None

                    results.append(playlist_data)

            if raw_data["next"]:
                raw_data = self.sp.next(raw_data)
            else:
                raw_data = None

        return results

    def identify_song(self, song):
        result = None
        clean_title = re.sub(r"[\(\[].*?[\)\]]", "", song["input_song_title"])
        input_artist_name = song.get("input_artist_name")
        if input_artist_name:
            raw_data = self.sp.search(
                q=f'{song["input_artist_name"]} {clean_title}',
                limit=1,
                type="track",
            )
        else:
            raw_data = self.sp.search(
                q=clean_title,
                limit=1,
                type="track",
            )

        if not raw_data["tracks"]["items"]:
            song["song_title"] = "None"
            print(f"{clean_title}, not found")
            return None

        result = self.parse_song_data(raw_data["tracks"]["items"][0])

        input_artist_name = song.get("input_artist_name")
        if input_artist_name:
            if not result["artist_name"].lower() == song["input_artist_name"].lower():
                pprint(
                    f'{song["input_artist_name"]} =/= {result["artist_name"].lower()} {clean_title}, not found'
                )
                song["song_title"] = "None"
                return None
        db_song_id = song.get("db_song_id")
        if db_song_id:
            result["db_song_id"] = song["db_song_id"]

        return result

    def songs_from_list(self, title_list):
        return self.identify_songs([{"input_song_title": title} for title in title_list])

    def push_playlist(self, playlist):
        pass
