from modules.cache import cache
from rich.pretty import pprint
from ytmusicapi import YTMusic, OAuthCredentials

SERVICE_ID = "youtube"

default_config = {
    "enabled": True,
    "auth_token": "",
}

def init_config(config):
    global _config
    _config = config
    print(_config )
    


# we basically don't want a limit
REQUEST_SIZE_LIMIT = 10**5

yt = YTMusic("browser.json")

# playlistId = yt.create_playlist('test', 'test description')
# search_results = yt.search('Oasis Wonderwall')
# yt.add_playlist_items(playlistId, [search_results[0]['videoId']])


def ping():
    print(SERVICE_ID)


def parse_song_data(song):
    parsed_data = {
        "service_id": SERVICE_ID,
        "artist_id": song["artists"][0]["id"],
        "artist_name": song["artists"][0]["name"],
        "song_id": song["videoId"],
        "song_title": song["title"],
    }

    return parsed_data


@cache
def pull_songs():
    clean_songs = []
    for song in yt.get_liked_songs(REQUEST_SIZE_LIMIT)["tracks"]:
        clean_songs.append(parse_song_data(song))
    return clean_songs


@cache
def pull_playlists():
    clean_playlists = []
    for playlist in yt.get_library_playlists(REQUEST_SIZE_LIMIT):
        playlist_data = {
            "service_id": SERVICE_ID,
            "playlist_id": playlist["playlistId"],
            "playlist_name": playlist["title"],
            "songs": [],
        }
        raw_playlist_data = yt.get_playlist(
            playlist_data["playlist_id"], REQUEST_SIZE_LIMIT
        )
        for song in raw_playlist_data["tracks"]:
            playlist_data["songs"].append(parse_song_data(song))
        clean_playlists.append(playlist_data)
    return clean_playlists


def identify_songs(unidentified_songs):
    pass


if __name__ == "__main__":
    ping()

    song_data = pull_songs()
    print(song_data[0], len(song_data))
    playlist_data = pull_playlists()
    print(playlist_data[0]["songs"][0], len(playlist_data))
    print([playlist["playlist_name"] for playlist in playlist_data])
