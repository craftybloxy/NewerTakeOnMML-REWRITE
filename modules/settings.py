import toml
import os
from modules.plugins_init_settings import plugins_constants, init_service_ids
list_of_all_services = ["db", "input"] + init_service_ids
list_of_all_pushable_service = list(set(list_of_all_services) - {"input"})


main_setting_default = {
    "save_all_playlists": True,
    "service_priority": list_of_all_services,
    "plugins_whitelist": [],
    "plugins_blacklist": [],
    "pull_from": list_of_all_services,
    "push_to": list_of_all_pushable_service
}

dev_setting_default = {"api_cache": False, "cache_folder": "cache"}


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
        default = getattr(plugin, "DEFAULT_SETTINGS", {})
        settings["plugins"].setdefault(name, default)

    # Save file
    with open(path, "w") as f:
        toml.dump(settings, f)
    return settings


# Initialize setting
settings = load_settings(plugins_constants, path="settings.toml")
