from plugins.youtube.main import Plugin

youtube_service = YouTubeService()
youtube_service.ping()

song_data = youtube_service.pull_songs()
print(song_data[0], len(song_data))
playlist_data = youtube_service.pull_playlists()
print(playlist_data[0]["songs"][0], len(playlist_data))
print([playlist["playlist_name"] for playlist in playlist_data])
