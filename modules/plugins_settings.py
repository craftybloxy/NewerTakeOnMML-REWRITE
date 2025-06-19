import sys
import os
import importlib


def find_plugins_path():
    """ 
    finds the name of all available plugins
    
    Returns:
        list: a list of plugins's name
    """
    sys.path.append("./plugins")
    return [
        f
        for f in os.listdir("plugins")
        if os.path.isdir(os.path.join("plugins", f))
        and os.path.exists(os.path.join("plugins", f, "main.py"))
    ]


def import_paths(paths, name):
    """
    import the plugin modules into a list using the plugin's name.
    The name must be in sys path.
    """

    return [importlib.import_module(f"{path}.{name}") for path in paths]


plugins_paths = find_plugins_path()
plugins_settings = import_paths(plugins_paths, "settings")

# get the service id from each plugins that will be used to initialise the settings file
service_ids_settings = [plugin.SERVICE_ID for plugin in plugins_settings]
