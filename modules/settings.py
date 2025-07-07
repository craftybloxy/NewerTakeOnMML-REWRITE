import toml
import os
from modules.plugins_init import plugins_constants, init_service_ids

list_of_all_services = ["db", "input"] + init_service_ids
list_of_all_pushable_service = list(set(list_of_all_services) - {"input"})


main_setting_default = {
    "save_all_playlists": True,
    "service_priority": list_of_all_services,
    "plugins_whitelist": [],
    "plugins_blacklist": [],
    "pull_from": list_of_all_services,
    "push_to": list_of_all_pushable_service,
}

instance_count_default = {service: 1 for service in init_service_ids}

debug_setting_default = {"api_cache": False, "cache_folder": "cache"}


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
    settings.setdefault("debug", debug_setting_default)
    settings.setdefault("instance_count", instance_count_default)
    settings.setdefault("instances", {})

    # Add plugin's defaults settings in new format
    for plugin in plugins_settings:
        service_id = plugin.SERVICE_ID
        num_instances = settings["instance_count"][service_id]

        # Initialize service list if it doesn't exist
        if service_id not in settings["instances"]:
            settings["instances"][service_id] = []

        # Ensure we have the right number of instances
        current_count = len(settings["instances"][service_id])
        if current_count < num_instances:
            # Add missing instances
            default = getattr(plugin, "DEFAULT_SETTINGS", {})
            for i in range(current_count, num_instances):
                settings["instances"][service_id].append(default.copy())
        elif current_count > num_instances:
            # Remove excess instances
            settings["instances"][service_id] = settings["instances"][service_id][
                :num_instances
            ]

    # Save file
    with open(path, "w") as f:
        toml.dump(settings, f)
    return settings


# Initialize setting
settings = load_settings(plugins_constants, path="settings.toml")
