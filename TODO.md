[ ] Add a database (songs: url[spotify,path]), (playlists: songs)
[ ] Make a plugin template for data (fetch/push) (all; saved: songs, albums, artists, playlists)
[ ] Make the spotify plugin
[ ] Make the local plugin
[ ] Link playlists together
[ ] Add a config file
[ ] add a way to link playlists
[ ] Make the plugin template for downloading


> disc_number? ou index indépendant

plugin data
    artist
        artistid
        name
    artist_alt
        alt name
        url
    
    album
        albumid
        name
        artistid
        year
        genre
        description

    album_alt
        url
        alt name

    album_index
        albumid
        musicid

    music
        musicid
        name
        albumid
        artistid
        year
        genre
        description
        duration

    music_alt
        url
        alt name

    playlist
        name
        author
        date created
        description

    playlist_index
        music_id
        playlist_id
        date_added

    playlist_alt
        url
        alt name
        

plugin functions
    pull
        all saved artists
        all saved albums
        all saved music
        all personal playlists
        all saved playlists
        one albums
        one music
        one playlists
    push
        all saved artists
        all saved albums
        all saved music
        all personal playlists
        all saved playlists
        one albums
        one music
        one playlists

STEP 1:
Make the system work with song data

STEP 2: 