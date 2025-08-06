from modules.data.PlaylistRef import PlaylistRef

class Playlist:
    """
    A collection of unique songs using __eq__ for uniqueness instead of hashing.
    Handles merging of songs that become connected through shared references.
    """


    def __init__(self, service_id=None, songs=None, playlist_refs=None):
        """
        Object that represents a playlist or in other words a set of songs

        Args:
            songs (list, optional): list of Song objects in the playlist.
            service_id (str, optional): service_id of the original source.
            playlist_refs (list, optional): list of dictionaries {service_id:ref_dict, service_id:ref_dict ... }
        """
        self.service_id = service_id
        self.playlist_refs = playlist_refs
        self.songs = []
        if songs:
            self.add_list(songs)

    def add(self, song):
        """
        Add a song to the set, handling three cases:
        1. Song isn't in set - add it
        2. Song matches one existing song - merge them
        3. Song matches multiple existing songs - merge all of them

        Args:
            song (Song): The song object that is going to be added to the playlist

        Raises:
            TypeError: Can only add Song objects
        """
        if not isinstance(song, Song):
            raise TypeError("Can only add Song objects")

        # Find all songs that match the new song
        matching_indices = []
        for i, existing_song in enumerate(self.songs):
            if song == existing_song:
                matching_indices.append(i)
        if not matching_indices:
            # Case 1: Song isn't in the set, add it
            self.songs.append(song)
        elif len(matching_indices) == 1:
            # Case 2: Song matches one existing song, merge them
            index = matching_indices[0]
            self.songs[index].merge(song)
        else:
            # Case 3: Song matches multiple existing songs, merge all of them
            # Pop the smallest index and update that song directly
            smallest_index = matching_indices.pop(0)

            # Merge the new song into the existing song at smallest index
            self.songs[smallest_index].merge(song)

            # Merge all other matching songs into the song at smallest index (in reverse order)
            for index in reversed(matching_indices):
                self.songs[smallest_index].merge(self.songs[index])
                del self.songs[index]

    def add_list(self, songs):
        """Add multiple songs to the set."""
        for song in songs:
            self.add(song)

    def _intersection(self, other):
        """
        Return a new Playlist containing songs that exist in both playlists.

        Args:
            other (Playlist): Another playlist to intersect with

        Returns:
            Playlist: A new playlist containing common songs

        Raises:
            TypeError: If other is not a Playlist object
        """
        if not isinstance(other, Playlist):
            raise TypeError("Can only intersect with another Playlist object")

        # Create a new playlist for the result
        result = Playlist(
            service_id=self.service_id,
            songs=None,
            playlist_refs={**self.playlist_refs, **other.playlist_refs},
        )

        # Find songs that exist in both playlists
        for song_a in self.songs:
            for song_b in other.songs:
                if song_a == song_b:
                    result.add_list([song_a, song_b])

        return result

    def __and__(self, other):
        """
        Implement the & operator for _intersection.

        Args:
            other (Playlist): Another playlist to intersect with

        Returns:
            Playlist: A new playlist containing common songs
        """
        return self._intersection(other)

    def add_metadata_from(self, other):
        self.add_list(self & other)

    def __contains__(self, song):
        """Check if a song is in the set."""
        return song in self.songs

    def __iter__(self):
        """Iterate over songs in the set."""
        return iter(self.songs)

    def __len__(self):
        """Return the number of songs in the set."""
        return len(self.songs)

    def __repr__(self):
        """Detailed representation of the set."""
        return f"Playlist({self.songs})"

    def merge(self, other):
        if not isinstance(other, Playlist):
            raise TypeError("Can only add playlist objects together")
        self.add_list(other.songs)
        return self

    def __getitem__(self, key):
        """Make playlist subscriptable - supports indexing and slicing."""
        return self.songs[key]

    def __setitem__(self, key, value):
        """Allow item assignment via indexing."""
        if not isinstance(value, Song):
            raise TypeError("Can only assign Song objects")
        self.songs[key] = value

    def __delitem__(self, key):
        """Allow item deletion via indexing."""
        del self.songs[key]

    def __eq__(self, other):
        """
        Define equality based on id in db or matching refs.
        Songs are equal if they have the same id or share any matching ref data

        Args:
            other: Another object to compare with

        Returns:
            bool: True if equal, False otherwise
        """
        if not isinstance(other, Song):
            return False

        # Check if songs have same db id
        self_db_ref = self.playlist_refs.get("db")
        other_db_ref = other.playlist_refs.get("db")

        if self_db_ref and other_db_ref:
            if (
                self.playlist_refs["db"]["song_id"]
                == other.playlist_refs["db"]["song_id"]
            ):
                return True

        if self.playlist_refs and other.playlist_refs:
            for service_id, ref in self.playlist_refs.items():
                if service_id in other.playlist_refs:
                    bare_self_ref = self.playlist_refs[service_id].get("playlist_id")
                    bare_other_ref = other.playlist_refs[service_id].get("playlist_id")

                    if bare_self_ref == bare_other_ref:
                        return True
        return False

    def remove(self, song):
        """Remove a song from the set if it exists."""
        if song in self.songs:
            self.songs.remove(song)
        else:
            raise KeyError("Song not found in set")

    def discard(self, song):
        """Remove a song from the set if it exists, no error if not found."""
        if song in self.songs:
            self.songs.remove(song)

    def clear(self):
        """Remove all songs from the set."""
        self.songs.clear()

    def copy(self):
        return Playlist(
            service_id=self.service_id.copy(),
            songs=self.songs.copy(),
            playlist_refs=self.playlist_refs.copy(),
        )
