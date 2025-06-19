import toml
import os
from modules.plugins_settings import plugins_settings, service_ids_settings


main_setting_default = {
    "save_all_playlists": True,
    "service_priority": ["db", "input"] + service_ids_settings ,
    "plugins_whitelist": [],
    "plugins_blacklist": []
}

dev_setting_default = {
    "api_cache":False
}


def load_settings(plugins_settings, path="settings.toml"):
    """Loads and saves settings to the path using default settings as template

    Args:
        plugins_settings (list): a list of plugin setting objects
        path (str, optional): path to the plugin file. Defaults to "settings.toml".

    Returns:
        (settings): an object with all the program's settings
    """
    # Load existing setting or initialize a new one
    if os.path.exists(path):
        with open(path, "r") as f:
            settings = toml.load(f)
    else:
        settings = {}

    settings.setdefault("main", main_setting_default)
    settings.setdefault("dev", dev_setting_default)
    settings.setdefault("plugins", {})

    # Add plugin's defaults settings
    for plugin in plugins_settings:
        name = plugin.SERVICE_ID
        default = getattr(plugin, "default_settings", {})
        settings["plugins"].setdefault(name, default)

    # Save file
    with open(path, "w") as f:
        toml.dump(settings, f)

    return settings

# Initialize setting
settings = load_settings(plugins_settings,  path="settings.toml")