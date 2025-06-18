from modules.Song import Song

class Playlist:
    """
    A collection of unique songs using __eq__ for uniqueness instead of hashing.
    Handles merging of songs that become connected through shared references.
    """
    def __init__(self, songs=None, playlist_id=None, playlist_refs=None ):
        self.playlist_id = playlist_id
        self.playlist_ref = playlist_refs
        self._songs = []
        if songs:
            self.update(songs)
            
    def add(self, song):
        """
        Add a song to the set, handling three cases:
        1. Song isn't in set - add it
        2. Song matches one existing song - merge them
        3. Song matches multiple existing songs - merge all of them
        """
        if not isinstance(song, Song):
             raise TypeError("Can only add Song objects")

            
        
        # Find all songs that match the new song
        matching_indices = []
        for i, existing_song in enumerate(self._songs):
            if song == existing_song:
                matching_indices.append(i)
        
        if not matching_indices:
            # Case 1: Song isn't in the set, add it
            self._songs.append(song)
        elif len(matching_indices) == 1:
            # Case 2: Song matches one existing song, merge them
            index = matching_indices[0]
            self._songs[index] = self._songs[index] + song
        else:
            # Case 3: Song matches multiple existing songs, merge all of them
            # Start with the new song
            merged_song = song
            
            # Merge with all matching songs (in reverse order to maintain indices)
            for index in sorted(matching_indices, reverse=True):
                merged_song = merged_song + self._songs[index]
                # Remove the merged song from the list
                del self._songs[index]
            
            # Add the final merged song
            self._songs.append(merged_song)
            
    def update(self, songs):
        """Add multiple songs to the set."""
        for song in songs:
            self.add(song)
            
    def __contains__(self, song):
        """Check if a song is in the set."""
        return song in self._songs
        
    def __iter__(self):
        """Iterate over songs in the set."""
        return iter(self._songs)
        
    def __len__(self):
        """Return the number of songs in the set."""
        return len(self._songs)
        
    def __str__(self):
        """String representation of the set."""
        return f'{[song for song in self._songs]}'
        
    def __repr__(self):
        """Detailed representation of the set."""
        return f'SongSet({self._songs})'
        
    def __eq__(self, other):
        """Check equality with another SongSet."""
        if not isinstance(other, Playlist):
            return False
        return set(str(song) for song in self._songs) == set(str(song) for song in other._songs)
    
    def remove(self, song):
        """Remove a song from the set if it exists."""
        if song in self._songs:
            self._songs.remove(song)
        else:
            raise KeyError("Song not found in set")
    
    def discard(self, song):
        """Remove a song from the set if it exists, no error if not found."""
        if song in self._songs:
            self._songs.remove(song)
    
    def clear(self):
        """Remove all songs from the set."""
        self._songs.clear()
    
    def copy(self):
        """Create a shallow copy of the SongSet."""
        new_set = Playlist()
        new_set._songs = [song.copy() for song in self._songs]
        return new_set