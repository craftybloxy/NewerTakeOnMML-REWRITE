from modules.Song import Song


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
        self._songs = []
        if songs:
            self.update(songs)

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
        return f"{[song for song in self._songs]}"

    def __repr__(self):
        """Detailed representation of the set."""
        return f"SongSet({self._songs})"

    def __add__(self, other):
        if not other.isinstance(Playlist):
            raise TypeError("Can only add playlist objects together")
        self.add(other)

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

        # Check if songs share any matching refs
        if self.playlist_refs and other.playlist_refs:
            # Check if any service_id exists in both songs with matching data
            for service_id, ref in self.playlist_refs.items():
                # check if only essencial fields are the same
                if service_id in other.playlist_refs:
                    bare_self_ref = self.playlist_refs[service_id].get("playlist_id")
                    bare_other_ref = other.playlist_refs[service_id].get("playlist_id")

                    if bare_self_ref == bare_other_ref:
                        return True
        return False

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
