import plugins.spotify.main
from modules.utils import input_playlist

if __name__ == "__main__":
    song_data = pull_songs()
    print(song_data[0], len(song_data))
    playlist_data = pull_playlists()
    print(playlist_data[4]["songs"][0], len(playlist_data))
    ping()
