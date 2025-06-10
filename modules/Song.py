class Song(dict):
    """
    type de donnée utiliser pour une musique
    """

    def __init__(self, data: dict):
        """
        Adds the kwargs to the dict-like type
        """
        self["song_id"] = data.get("song_id", None)
        self["song_title"] = data.get("song_title", None)
        self["song_refs"] = data.get("song_refs", {})

    def refs(self):
        return self["song_refs"]

    def raw(self):
        return {
            "song_id": self["song_id"],
            "song_title": self["song_title"],
            "song_refs": self["song_refs"]
        }

    def __eq__(self, other):
        """
        Define equality based on id or matching refs.
        Songs are equal if they have the same id or share any matching ref data

        Args:
            other: Another object to compare with

        Returns:
            bool: True if equal, False otherwise
        """
        if not isinstance(other, Song):
            return False

        # Check if songs have same id
        if self["song_id"] and other["song_id"]:
            return self["song_id"] == other["song_id"]

        # Check if songs share any matching refs
        if self["song_refs"] and other["song_refs"]:
            # Check if any service_id exists in both songs with matching data
            for service_id, ref in self["song_refs"].items():
                if service_id in other["song_refs"]:
                    if ref == other["song_refs"][service_id]:
                        return True
        return False

    def __add__(self, other):
        """
        Merge two songs if they are equal (same ID or shared refs).
        The merged song will have:
        - The song_id from self if it exists, otherwise from other
        - The song_title from self if it exists, otherwise from other
        - All refs from both songs combined

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
            merged_data = {
                "song_id": self["song_id"] or other["song_id"],
                "song_title": self["song_title"] or other["song_title"],
                "song_refs": {**self["song_refs"], **other["song_refs"]}
            }
            return Song(merged_data)
        else:
            raise ValueError(
                "Can only merge songs that are equal (same ID or shared refs)"
            )

    def copy(self):
        """
        Creates a deep copy of the Song object.

        Returns:
            Song: A new Song instance with copied attributes
        """
        return Song(self.raw())

    def __repr__(self):
        return f'Song( {self["song_id"]}, {self["song_title"]}, {self.refs()})'
