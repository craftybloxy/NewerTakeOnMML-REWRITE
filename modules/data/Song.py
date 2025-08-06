from modules.SongRef import SongRef


class Song:
    """
    Datatype used to store one music and all of its refferences across services
    """

    def __init__(self, service_id=None, song_refs=None):
        """
        Adds the data to the song object

        Args:
            service_id (str): id of the original service
            song_refs (dict): dict of dictionaries {service_id:ref_dict, service_id:ref_dict ... }
        """
        if service_id is None:
            service_id = self._get_oldest_service_id()
        self.song_refs = song_refs
        self.service_id = service_id

    def _get_oldest_service_id(self):
        """
        Set the main service_id to the oldest "date_added" ref

        Returns:
            str: service_id of the ref with the oldest date_added
        """

        if not self.song_refs:
            self.service_id = None
            return
        items = [
            (service_id, ref.date_added) for service_id, ref in self.song_refs.items()
        ]
        oldest_service = items[0][0]
        for service, date_added in items[0:]:
            if date_added < self.song_refs[oldest_service].date_added:
                oldest_service = service
        return oldest_service

    def _get_oldest_date(self):
        return self.song_refs[self._get_oldest_service_id()].date_added

    def __eq__(self, other):
        """
        Define song equality based on if they have the same id or share any matching ref data

        Args:
            other: Another object to compare with

        Returns:
            bool: True if equal, False otherwise
        """
        if not isinstance(other, Song):
            return False

        # Check if songs share any matching refs
        if self.song_refs and other.song_refs:
            # Check if any service_id exists in both songs with matching data
            for service_id, ref in self.song_refs.items():
                # check if only essencial fields are the same
                if service_id in other.song_refs:
                    bare_self_ref = (
                        self.song_refs[service_id].artist_id,
                        self.song_refs[service_id].song_id,
                    )
                    bare_other_ref = (
                        other.song_refs[service_id].artist_id,
                        other.song_refs[service_id].song_id,
                    )

                    if bare_self_ref == bare_other_ref:
                        return True
        return False

    def merge(self, other):
        """
        Merge two songs if they are equal (at least one shared refs).
        The merged song will have all refs from both songs combined
        The service_id is changed to the oldest date_added in ref

        Args:
            other: Another Song object to merge with

        Raises:
            TypeError: If other is not a Song object
            ValueError: If songs are not equal (can't be merged)
        """
        if not isinstance(other, Song):
            print(self, other)
            raise TypeError("Can only add Song objects together")
        
        if other._get_oldest_date() < self._get_oldest_date():
            if other.service_id is not None:
                self.service_id = other.service_id
        
        for key_service_id in other.song_refs.keys():
            self_ref = self.song_refs.get(key_service_id, SongRef())
            other_ref = other.song_refs.get(key_service_id, SongRef())
            self.song_refs[key_service_id] = self_ref.merge(other_ref)

    def copy(self):
        """
        Creates a shallow copy of the Song object.

        Returns:
            Song: A new Song instance with copied attributes
        """
        return Song(self.service_id, self.song_refs.copy())

    def __repr__(self):
        return f"Song({self.service_id}, {self.song_refs.keys()})"
