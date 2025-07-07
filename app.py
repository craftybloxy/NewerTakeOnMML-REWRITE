from modules.database import Database
from rich.pretty import pprint
from modules.plugins import plugins, service_ids
from modules.settings import settings

class Plugin_wrapper:
    def __init__(self):
        self.db = Database(service_ids, "library.db")

    def ping(self):
        for plugin in plugins:
            plugin.ping()

    def pull_songs(self):
        print("pull_songs")
        all_songs = []
        for plugin in plugins:
            all_songs.extend(plugin.pull_songs())

        print("saving to db..")
        self.db.insert_songs(all_songs)

    def pull_playlists(self):
        print("pull_playlists")
        all_playlists = []
        for plugin in plugins:
            all_playlists.extend(plugin.pull_playlists())

        print("saving to db..")
        self.db.insert_playlists(all_playlists)

    def identify_songs(self):
        print("identify_songs")
        result = []
        for plugin in plugins :
            unidentified_songs = self.db.fetch_unidentified_songs(plugin.SERVICE_ID)
            
            # For every unidentified song, identifie using the plugin's method 
            newly_identified_songs = []
            
            
            counter = 0
            print(len(unidentified_songs))
            
            
            
            for song in unidentified_songs:
                identified_song = plugin.identify_song(song)
                if identified_song:
                    newly_identified_songs.append(identified_song)
                    
                    
                counter += 1
                print(f"{counter}/{len(unidentified_songs)}")


            if newly_identified_songs:
                result.extend(newly_identified_songs)
        print("saving to db..")

        self.db.insert_songs(result)

    def identify_playlists(self):
        pass


app = Plugin_wrapper()
app.pull_songs()
#app.pull_playlists()
app.identify_songs()
print(app.db.find_duplicates("artists","name", "id"))
#app.ping()

