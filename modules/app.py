def input_multiline(message):
    print(message, end="")
    result = []
    while True:
        user_input = input()
        if user_input == "":
            break
        else:
            result.append(user_input)
    return result

def input_playlist(song_from_list):
    playlist_name = input("playlist name: ")
    raw_songs = input_multiline("songs (one per line): ")
    songs = songs_from_list(raw_songs)
    return {"playlist_name": playlist_name, "songs": songs}