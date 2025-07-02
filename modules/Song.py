from modules.SongRef import SongRef

class Song:
    """
    Datatype used to store one music and all of its refferences across services
    """

    def __init__(self, service_id, song_refs=None):
        """
        Adds the data to the song object

        Args:
            service_id (str): id of the original service
            song_refs (dict): dict of dictionaries {service_id:ref_dict, service_id:ref_dict ... }
        """
        self.song_refs = song_refs
        self.service_id = self.get_oldest_service_id()

    def get_oldest_service_id(self):
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

    def get_oldest_date(self):
        return self.song_refs[self.get_oldest_service_id()].date_added

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
        self_db_ref = self.song_refs.get("db")
        other_db_ref = other.song_refs.get("db")

        if self_db_ref and other_db_ref:
            if self.song_refs["db"]["song_id"] == other.song_refs["db"]["song_id"]:
                return True

        # Check if songs share any matching refs
        if self.song_refs and other.song_refs:
            # Check if any service_id exists in both songs with matching data
            for service_id, ref in self.song_refs.items():
                # check if only essencial fields are the same
                if service_id in other.song_refs:
                    bare_self_ref = (
                        self.song_refs[service_id].artist_id,
                        self.song_refs[service_id].artist_name,
                        self.song_refs[service_id].song_id,
                        self.song_refs[service_id].song_title,
                    )
                    bare_other_ref = (
                        other.song_refs[service_id].artist_id,
                        other.song_refs[service_id].artist_name,
                        other.song_refs[service_id].song_id,
                        other.song_refs[service_id].song_title,
                    )

                    if bare_self_ref == bare_other_ref:
                        return True
        return False

    def __add__(self, other):
        """
        Merge two songs if they are equal (at least one shared refs).
        The merged song will have all refs from both songs combined
        The service_id is changed to the oldest date_added in ref

        Args:
            other: Another Song object to merge with

        Returns:
            Song: A new Song instance with merged data

        Raises:
            TypeError: If other is not a Song object
            ValueError: If songs are not equal (can't be merged)
        """
        if not isinstance(other, Song):
            raise TypeError("Can only add Song objects together")

        if self == other:
            if self.get_oldest_date() < other.get_oldest_date():
                if self.service_id is not None:
                    service_id = self.service_id
                else:
                    service_id = other.service_id

            else:
                if other.service_id is not None:
                    service_id = other.service_id
                else:
                    service_id = self.service_id

            song_refs = {}
            # merge metadata
            for key_service_id in self.song_refs.keys() | other.song_refs.keys():
                self_ref = self.song_refs.get(key_service_id, SongRef())
                other_ref = other.song_refs.get(key_service_id, SongRef())
                song_refs[key_service_id] = self_ref + other_ref
            return Song(self.service_id, song_refs)
        
        else:
            raise ValueError(
                "Can only merge songs that are equal (same ID or shared refs)"
            )

    def copy(self):
        """
        Creates a shallow copy of the Song object.

        Returns:
            Song: A new Song instance with copied attributes
        """
        return Song(self.service_id, self.song_refs.copy())

    def __repr__(self):
        return f"Song({self.service_id}, {self.song_refs.keys()})"
