import toml
import os
from modules.plugins import plugins, service_ids


main_setting_default = {
    "save_all_playlists": True,
    "service_priority": ["db", "user"] + service_ids ,
}

def load_settings(plugins, path="settings.toml"):
    # Load existing setting or initialize a new one
    if os.path.exists(path):
        with open(path, "r") as f:
            settings = toml.load(f)
    else:
        settings = {}

    settings.setdefault("main", main_setting_default)
    settings.setdefault("plugins", {})

    # Add plugin's defaults settings
    for plugin in plugins:
        name = plugin.SERVICE_ID
        default = getattr(plugin, "default_settings", {})
        settings["plugins"].setdefault(name, default)

    # Save file
    with open(path, "w") as f:
        toml.dump(settings, f)

    return settings

# Initialize setting
settings = load_settings(plugins,  path="settings.toml")
