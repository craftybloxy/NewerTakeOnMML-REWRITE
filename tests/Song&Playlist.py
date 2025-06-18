import pytest
from modules.Song import Song
from modules.Playlist import Playlist


class TestSong:
    """Test cases for the Song class"""
    
    def test_song_creation_with_id_and_refs(self):
        """Test creating a song with both ID and refs"""
        song_refs = {
            "spotify": {
                "artist_id": "test_artist",
                "song_id": "test_song",
                "song_title": "Test Song"
            }
        }
        song = Song(song_id=1, song_refs=song_refs)
        
        assert song.song_id == 1
        assert song.song_refs == song_refs
        assert song.refs() == song_refs
    
    def test_song_creation_with_only_refs(self):
        """Test creating a song with only refs (no ID)"""
        song_refs = {
            "youtube": {
                "artist_id": "test_artist",
                "song_id": "test_song"
            }
        }
        song = Song(song_id=None, song_refs=song_refs)
        
        assert song.song_id is None
        assert song.song_refs == song_refs
    
    def test_song_equality_same_id(self):
        """Test that songs with same ID are equal"""
        song1 = Song(song_id=1, song_refs={"spotify": {"id": "a"}})
        song2 = Song(song_id=1, song_refs={"youtube": {"id": "b"}})
        
        assert song1 == song2
    
    def test_song_equality_shared_refs(self):
        """Test that songs with matching refs are equal"""
        refs1 = {
            "spotify": {
                "artist_id": "yonakgor",
                "song_id": "s1",
                "song_title": "Another Mistake"
            }
        }
        refs2 = {
            "spotify": {
                "artist_id": "yonakgor", 
                "song_id": "s1",
                "song_title": "Another Mistake"
            },
            "youtube": {
                "artist_id": "yonakgor",
                "song_id": "different_id"
            }
        }
        
        song1 = Song(song_id=None, song_refs=refs1)
        song2 = Song(song_id=None, song_refs=refs2)
        
        assert song1 == song2
    
    def test_song_inequality_no_matching_refs_or_id(self):
        """Test that songs with no matching refs or ID are not equal"""
        song1 = Song(song_id=1, song_refs={"spotify": {"id": "a"}})
        song2 = Song(song_id=2, song_refs={"youtube": {"id": "b"}})
        assert not song1 == song2
    
    def test_song_inequality_with_non_song_object(self):
        """Test that song is not equal to non-Song objects"""
        song = Song(song_id=1, song_refs={})
        
        assert song != "not a song"
        assert song != 123
        assert song != None
    
    def test_song_addition_equal_songs(self):
        """Test merging two equal songs"""
        song1 = Song(
            song_id=1,
            song_refs={"spotify": {"id": "a", "title": "Test"}}
        )
        song2 = Song(
            song_id=None,
            song_refs={"youtube": {"id": "b", "title": "Test"}}
        )
        
        # Make them equal by giving them matching refs
        song2.song_id = 1
        
        merged = song1 + song2
        
        assert merged.song_id == 1
        assert "spotify" in merged.song_refs
        assert "youtube" in merged.song_refs
    
    def test_song_addition_unequal_songs_raises_error(self):
        """Test that adding unequal songs raises ValueError"""
        song1 = Song(song_id=1, song_refs={"spotify": {"id": "a"}})
        song2 = Song(song_id=2, song_refs={"youtube": {"id": "b"}})
        
        with pytest.raises(ValueError, match="Can only merge songs that are equal"):
            song1 + song2
    
    def test_song_addition_with_non_song_raises_error(self):
        """Test that adding non-Song object raises TypeError"""
        song = Song(song_id=1, song_refs={})
        
        with pytest.raises(TypeError, match="Can only add Song objects together"):
            song + "not a song"

class TestPlaylist:
    """Test cases for the Playlist class"""
    
    @pytest.fixture
    def sample_songs(self):
        """Fixture providing sample songs for testing"""
        another_mistake = Song(
            song_id=1,
            song_refs={
                "youtube": {
                    "artist_id": "yonakgor",
                    "artist_name": "Yonakgor", 
                    "song_id": "s1",
                    "song_title": "Another Mistake",
                },
                "spotify": {
                    "artist_id": "yonakgor",
                    "artist_name": "Yonakgor",
                    "song_id": "s1", 
                    "song_title": "Another Mistake",
                },
            }
        )
        
        another_mistake_alt = Song(
            song_id=None,
            song_refs={
                "soundcloud": {
                    "artist_id": "yonakgor",
                    "artist_name": "Yonakgor",
                    "song_id": "s1",
                    "song_title": "Another Mistake",
                },
                "spotify": {
                    "artist_id": "yonakgor", 
                    "artist_name": "Yonakgor",
                    "song_id": "s1",
                    "song_title": "Another Mistake",
                },
            }
        )
        
        nothing = Song(
            song_id=2,
            song_refs={
                "spotify": {
                    "artist_id": "kennyoung",
                    "artist_name": "Kennyoung",
                    "song_id": "s3",
                    "song_title": "Nothing",
                },
                "youtube": {
                    "artist_id": "kennyoung",
                    "artist_name": "Kennyoung", 
                    "song_id": "s3",
                    "song_title": "Nothing",
                },
            }
        )
        
        nothing_alt = Song(
            song_id=3,
            song_refs={
                "deezer": {
                    "artist_id": "kennyoung",
                    "artist_name": "Kennyoung",
                    "song_id": "s2", 
                    "song_title": "Nothing",
                },
                "apple_music": {
                    "artist_id": "kennyoung",
                    "artist_name": "Kennyoung",
                    "song_id": "s4",
                    "song_title": "Nothing",
                },
            }
        )
        
        bridge_song = Song(
            song_id=None,
            song_refs={
                "spotify": {
                    "artist_id": "yonakgor",
                    "artist_name": "Yonakgor",
                    "song_id": "s1",
                    "song_title": "Another Mistake",
                },
                "deezer": {
                    "artist_id": "kennyoung",
                    "artist_name": "Kennyoung",
                    "song_id": "s2",
                    "song_title": "Nothing",
                },
            }
        )
        
        unique_song = Song(
            song_id=42,
            song_refs={
                "bandcamp": {
                    "artist_id": "unique_artist",
                    "artist_name": "Unique Artist",
                    "song_id": "unique_id",
                    "song_title": "Unique Song",
                }
            }
        )
        
        return {
            'another_mistake': another_mistake,
            'another_mistake_alt': another_mistake_alt,
            'nothing': nothing,
            'nothing_alt': nothing_alt,
            'bridge_song': bridge_song,
            'unique_song': unique_song
        }
    
    def test_playlist_creation_empty(self):
        """Test creating an empty playlist"""
        playlist = Playlist()
        
        assert len(playlist) == 0
        assert list(playlist) == []
    
    def test_playlist_creation_with_songs(self, sample_songs):
        """Test creating playlist with initial songs"""
        songs = [sample_songs['unique_song'], sample_songs['another_mistake']]
        playlist = Playlist(songs=songs)
        
        assert len(playlist) == 2
        assert sample_songs['unique_song'] in playlist
        assert sample_songs['another_mistake'] in playlist
    
    def test_playlist_creation_with_metadata(self):
        """Test creating playlist with ID and refs"""
        playlist = Playlist(
            playlist_id="test_playlist",
            playlist_refs={"spotify": "playlist_123"}
        )
        
        assert playlist.playlist_id == "test_playlist"
        assert playlist.playlist_ref == {"spotify": "playlist_123"}
    
    def test_add_unique_song(self, sample_songs):
        """Test Case 1: Adding a song that isn't in the playlist"""
        playlist = Playlist()
        
        playlist.add(sample_songs['unique_song'])
        
        assert len(playlist) == 1
        assert sample_songs['unique_song'] in playlist
    
    def test_add_matching_song_single_merge(self, sample_songs):
        """Test Case 2: Adding a song that matches one existing song"""
        playlist = Playlist()
        playlist.add(sample_songs['another_mistake'])
        
        assert len(playlist) == 1
        
        # Add matching song - should merge
        playlist.add(sample_songs['another_mistake_alt'])
        
        assert len(playlist) == 1  # Still only one song
        
        # Check that the song was merged (has refs from both)
        merged_song = list(playlist)[0]
        assert "youtube" in merged_song.song_refs
        assert "spotify" in merged_song.song_refs
        assert "soundcloud" in merged_song.song_refs
    
    def test_add_bridge_song_multiple_merge(self, sample_songs):
        """Test Case 3: Adding a song that matches multiple existing songs"""
        playlist = Playlist()
        
        # Add two separate songs
        playlist.add(sample_songs['another_mistake'])
        playlist.add(sample_songs['nothing_alt'])
        
        assert len(playlist) == 2
        
        # Add bridge song that connects both
        playlist.add(sample_songs['bridge_song'])
        
        assert len(playlist) == 1  # Should merge all three into one
        
        # Check that merged song has refs from all three
        merged_song = list(playlist)[0]
        assert "youtube" in merged_song.song_refs  # from another_mistake
        assert "spotify" in merged_song.song_refs   # from bridge_song
        assert "deezer" in merged_song.song_refs    # from bridge_song & nothing_alt
        assert "apple_music" in merged_song.song_refs  # from nothing_alt
    
    def test_add_non_song_raises_error(self):
        """Test that adding non-Song object raises TypeError"""
        playlist = Playlist()
        
        with pytest.raises(TypeError, match="Can only add Song objects"):
            playlist.add("not a song")
    
    def test_update_multiple_songs(self, sample_songs):
        """Test adding multiple songs via update method"""
        playlist = Playlist()
        songs = [
            sample_songs['another_mistake'],
            sample_songs['another_mistake_alt'],
            sample_songs['unique_song']
        ]
        
        playlist.update(songs)
        
        assert len(playlist) == 2  # another_mistake songs should merge
        assert sample_songs['unique_song'] in playlist
    
    def test_contains_operation(self, sample_songs):
        """Test __contains__ method"""
        playlist = Playlist([sample_songs['unique_song']])
        
        assert sample_songs['unique_song'] in playlist
        assert sample_songs['another_mistake'] not in playlist
    
    def test_iteration(self, sample_songs):
        """Test iterating over playlist"""
        songs = [sample_songs['unique_song'], sample_songs['another_mistake']]
        playlist = Playlist(songs)
        
        song_list = list(playlist)
        assert len(song_list) == 2
        assert all(isinstance(song, Song) for song in song_list)
    
    def test_string_representation(self, sample_songs):
        """Test string representation of playlist"""
        playlist = Playlist([sample_songs['unique_song']])
        
        str_repr = str(playlist)
        assert "Song(" in str_repr
        assert str(sample_songs['unique_song'].song_id) in str_repr
    
    def test_remove_existing_song(self, sample_songs):
        """Test removing a song that exists in playlist"""
        playlist = Playlist([sample_songs['unique_song']])
        
        assert len(playlist) == 1
        playlist.remove(sample_songs['unique_song'])
        assert len(playlist) == 0
    
    def test_remove_nonexistent_song_raises_error(self, sample_songs):
        """Test that removing non-existent song raises KeyError"""
        playlist = Playlist()
        
        with pytest.raises(KeyError, match="Song not found in set"):
            playlist.remove(sample_songs['unique_song'])
    
    def test_discard_existing_song(self, sample_songs):
        """Test discarding a song that exists"""
        playlist = Playlist([sample_songs['unique_song']])
        
        playlist.discard(sample_songs['unique_song'])
        assert len(playlist) == 0
    
    def test_discard_nonexistent_song_no_error(self, sample_songs):
        """Test that discarding non-existent song doesn't raise error"""
        playlist = Playlist()
        
        # Should not raise any exception
        playlist.discard(sample_songs['unique_song'])
        assert len(playlist) == 0
    
    def test_clear_playlist(self, sample_songs):
        """Test clearing all songs from playlist"""
        playlist = Playlist([sample_songs['unique_song'], sample_songs['another_mistake']])
        
        assert len(playlist) == 2
        playlist.clear()
        assert len(playlist) == 0
    
    def test_copy_playlist(self, sample_songs):
        """Test copying a playlist"""
        original = Playlist([sample_songs['unique_song']])
        copied = original.copy()
        
        assert len(copied) == len(original)
        assert copied is not original
        assert copied._songs is not original._songs
        
        # Songs should be copies, not references
        original_song = list(original)[0]
        copied_song = list(copied)[0]
        assert copied_song is not original_song
    
    def test_complex_three_way_merge(self):
        """Test complex scenario where one song connects three separate songs"""
        # Create three initially separate songs
        song_a = Song(
            song_id=100,
            song_refs={"spotify": {"id": "a1", "title": "Song A"}}
        )
        song_b = Song(
            song_id=200,
            song_refs={"youtube": {"id": "b1", "title": "Song B"}}
        )
        song_c = Song(
            song_id=300,
            song_refs={"apple_music": {"id": "c1", "title": "Song C"}}
        )
        
        # Bridge song that connects all three
        mega_bridge = Song(
            song_id=None,
            song_refs={
                "spotify": {"id": "a1", "title": "Song A"},
                "youtube": {"id": "b1", "title": "Song B"},
                "apple_music": {"id": "c1", "title": "Song C"}
            }
        )
        
        playlist = Playlist()
        playlist.add(song_a)
        playlist.add(song_b)
        playlist.add(song_c)
        
        assert len(playlist) == 3
        
        # Adding mega bridge should merge all four songs into one
        playlist.add(mega_bridge)
        
        assert len(playlist) == 1
        
        # Verify all refs are present in the merged song
        merged_song = list(playlist)[0]
        assert "spotify" in merged_song.song_refs
        assert "youtube" in merged_song.song_refs
        assert "apple_music" in merged_song.song_refs
    
    def test_edge_case_empty_song(self):
        """Test handling of songs with no ID or refs"""
        empty_song = Song(song_id=None, song_refs={})
        playlist = Playlist()
        
        playlist.add(empty_song)
        assert len(playlist) == 1
        
        # Adding another empty song should not merge (no matching criteria)
        another_empty = Song(song_id=None, song_refs={})
        playlist.add(another_empty)
        assert len(playlist) == 2
    
    def test_song_with_only_id(self):
        """Test handling of songs with only ID (no refs)"""
        id_only_song = Song(song_id=999, song_refs={})
        playlist = Playlist()
        
        playlist.add(id_only_song)
        assert len(playlist) == 1
        
        # Adding song with same ID should merge
        same_id_song = Song(song_id=999, song_refs={"spotify": {"id": "test"}})
        playlist.add(same_id_song)
        assert len(playlist) == 1
        
        merged_song = list(playlist)[0]
        assert merged_song.song_id == 999
        assert "spotify" in merged_song.song_refs


if __name__ == "__main__":
    pytest.main([__file__, "-v"])