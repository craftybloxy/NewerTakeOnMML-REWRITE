from modules.Song import Song

class SongSet:
    """
    A collection of unique songs using __eq__ for uniqueness instead of hashing.
    """
    def __init__(self, songs=None):
        self._songs = []
        if songs:
            self.update(songs)
            
    def add(self, song):
        if not isinstance(song, Song):
            raise TypeError("Can only add Song objects")
            
        for i in range(len(self._songs)):
            if song == self._songs[i]:
                self._songs[i] = self._songs[i] + song
                return
                
        self._songs.append(song)
            
    def update(self, songs):
        for song in songs:
            self.add(song)
            
    def __contains__(self, song):
        return song in self._songs
    def __iter__(self):
        return iter(self._songs)
    def __len__(self):
        return len(self._songs)
    def __repr__(self):
        return f'SongSet({self._songs})'
    def __str__(self):
        return f'{[(song.raw()["song_id"], song.raw()["song_title"]) for song in self._songs]}'
    def __eq__(self, other):
        return self._songs == other._songs
