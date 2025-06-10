import os
from tinytag import TinyTag
    
path = "/home/crafty/Music/Flacs/Shared Tunes"

def ping():
    print("Local")



def identify_songs():

    data = [
    {"identifiers": ["id1", "id2"], "name": "Name1"},
    {"identifiers": ["id3", "id4"], "name": "Name2"}
    ]
    # Walk through all subdirectories and files
    for root, _, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Process only files with audio extensions
            if filename.lower().endswith(('.mp3', '.flac', '.wav', '.aac', '.ogg', '.m4a')):
                try:
                    tag = TinyTag.get(file_path)  # Extract metadata
                    print(f"File: {file_path}")
                    print(f"Title: {tag.title}")
                    print(f"Artist: {tag.artist}")
                    print(f"Album: {tag.album}")
                    print(f"Duration: {tag.duration:.2f} seconds")
                    print("-" * 30)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    identify_songs()
