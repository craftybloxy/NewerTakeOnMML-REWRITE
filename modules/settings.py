import toml
import os

main_config_default = {
    "save_all_playlists": True,
    "service_priority": [],
}

def load_and_merge_plugin_settings(plugins, path="settings.toml"):
    # Load existing config or initialize a new one
    if os.path.exists(path):
        with open(path, "r") as f:
            config = toml.load(f)
    else:
        config = {}

    config.setdefault("main", main_config_default)
    config.setdefault("plugins", {})

    # Inject missing plugin config defaults
    for plugin in plugins:
        name = plugin.__name__
        default = getattr(plugin, "default_config", {})
        config["plugins"].setdefault(name, default)

    # Save back
    with open(path, "w") as f:
        toml.dump(config, f)

    return config
