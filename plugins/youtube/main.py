from modules.cache import cache
from rich.pretty import pprint
from ytmusicapi import YTMusic, OAuthCredentials
from plugins.youtube.settings import SERVICE_ID, REQUEST_SIZE_LIMIT


class Plugin:
    def __init__(self, ):
        self.yt = YTMusic("browser.json")
    
    def ping(self):
        print(self.SERVICE_ID)
    
    def parse_song_data(self, song):
        parsed_data = {
            "service_id": self.SERVICE_ID,
            "artist_id": song["artists"][0]["id"],
            "artist_name": song["artists"][0]["name"],
            "song_id": song["videoId"],
            "song_title": song["title"],
        }
        return parsed_data
    
    @cache
    def pull_songs(self):
        clean_songs = []
        for song in self.yt.get_liked_songs(self.REQUEST_SIZE_LIMIT)["tracks"]:
            clean_songs.append(self.parse_song_data(song))
        return clean_songs
    
    @cache
    def pull_playlists(self):
        clean_playlists = []
        for playlist in self.yt.get_library_playlists(self.REQUEST_SIZE_LIMIT):
            playlist_data = {
                "service_id": self.SERVICE_ID,
                "playlist_id": playlist["playlistId"],
                "playlist_name": playlist["title"],
                "songs": [],
            }
            raw_playlist_data = self.yt.get_playlist(
                playlist_data["playlist_id"], self.REQUEST_SIZE_LIMIT
            )
            for song in raw_playlist_data["tracks"]:
                playlist_data["songs"].append(self.parse_song_data(song))
            clean_playlists.append(playlist_data)
        return clean_playlists
    
    def identify_songs(self, unidentified_songs):
        pass

