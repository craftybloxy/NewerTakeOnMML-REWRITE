import sys
import os
import importlib

# Get a list of plugin folders in ./plugins
plugins_paths = [
    f for f in os.listdir("plugins") 
    if os.path.isdir(os.path.join("plugins", f)) 
    and os.path.exists(os.path.join("plugins", f, "main.py"))
]

# FOR TESTING PURPOSES
plugins_paths = ["spotify", "youtube"]

sys.path.append("./plugins")
# import the plugin modules into a list using the plugin's name
plugins = []
for plugin_name in plugins_paths:
    plugin = importlib.import_module(f"{plugin_name}.main")
    plugins.append(plugin)

# get the service id from each plugins that will be used to initialise the database
service_ids = [plugin.SERVICE_ID for plugin in plugins]
