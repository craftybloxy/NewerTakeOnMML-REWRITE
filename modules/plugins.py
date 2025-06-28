from modules.plugins_init_settings import plugins_paths, import_paths
from modules.settings import settings

#only activates plugin that are whitelisted and not blacklisted
if settings["main"]["plugins_whitelist"] == []:
    active_plugins_path = list(set(plugins_paths) - set(settings["main"]["plugins_blacklist"]))
else:
    active_plugins_path = list(set(plugins_paths) & set(settings["main"]["plugins_whitelist"]) - set(settings["main"]["plugins_blacklist"]))
    
#imports the plugins
plugins = import_paths(active_plugins_path, "main")
plugins_constants = import_paths(active_plugins_path, "settings")
# get the service id from each plugins that will be used to initialise the database

service_ids = [plugin.SERVICE_ID for plugin in plugins_constants]