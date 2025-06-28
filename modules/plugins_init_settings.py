import sys
import os
import importlib


def find_plugins_path():
    """ 
    finds the name of all available plugins in the ./plugins folder of the main module
    
    Returns:
        list: a list of plugin names
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
    Import the plugin modules into a list using the plugin's name.
    The plugins folder must already be in sys path.

    Args:
        paths (set): set of module paths
        name (str): name of the imported file inside the module

    Returns:
        list: list of imported module file
    """

    return [importlib.import_module(f"{path}.{name}") for path in paths]


plugins_paths = find_plugins_path()
plugins_constants = import_paths(plugins_paths, "settings")
# get the service id from each plugins that will be used to initialise the settings file
init_service_ids = [plugin.SERVICE_ID for plugin in plugins_constants]
