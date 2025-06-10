
import sys
import os
import importlib
from modules.database import Database
from rich.pretty import pprint
from modules.settings import load_and_merge_plugin_settings

class Plugin_wrapper:
    def __init__(self):
        # Get a list of the python files in ./plugins and list them as plugin names
        plugins = [
            f.replace(".py", "") for f in os.listdir("plugins") if f.endswith(".py")
        ]
        plugins = ["spotify", "youtube"]  # FOR TESTING PURPOSES

        sys.path.append("./plugins")
        # import the plugin modules into a list using the plugin's name
        self.plugins = [importlib.import_module(plugin) for plugin in plugins]

        self.settings = load_and_merge_plugin_settings(self.plugins)
        print(self.settings)
        # Inject config into plugins
        for plugin in self.plugins:
            plugin_name = plugin.__name__
            plugin.init_config(self.settings["plugins"].get(plugin_name, {}))
                
        # get the service id from each plugins that will be used to initialise the database
        service_ids = [plugin.SERVICE_ID for plugin in self.plugins]
        service_ids = ["spotify", "youtube"]
        self.db = Database(service_ids, "library.db")

    def ping(self):
        for plugin in self.plugins:
            plugin.ping()

    def pull_songs(self):
        print("pull_songs")
        all_songs = []
        for plugin in self.plugins:
            all_songs.extend(plugin.pull_songs())

        print("saving to db..")
        self.db.insert_songs(all_songs)

    def pull_playlists(self):
        print("pull_playlists")
        all_playlists = []
        for plugin in self.plugins:
            all_playlists.extend(plugin.pull_playlists())

        print("saving to db..")
        self.db.insert_playlists(all_playlists)

    def identify_songs(self):
        print("identify_songs")
        result = []
        for plugin in self.plugins[:1]:
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
        #pprint(result)
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

