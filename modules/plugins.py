from modules.plugins_settings import plugins_paths, import_paths

plugins = import_paths(plugins_paths, "main")
# get the service id from each plugins that will be used to initialise the databse
service_ids = [plugin.SERVICE_ID for plugin in plugins_settings]