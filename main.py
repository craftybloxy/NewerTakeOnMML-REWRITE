import logging
import sys
import importlib
plugins = ["default","alt"]
class Plugin_wrapper:
    # We are going to receive a list of plugins as parameter
    def __init__(self, plugins: list = []):
        # adds the plugin folder to path
        sys.path.append('./plugins')
        # Checking if plugins were sent
        if plugins:
            # create a list of plugins
            print("selected plugins:",plugins)
            self._plugins = [
                importlib.import_module(plugin, "./plugins/").Plugin() for plugin in plugins
            ]
        else:
            # If no plugins were set, we use our default which just prints test data
            logging.warning('no plugin selected, using default fallback')
            self._plugins = [importlib.import_module('default', "./plugins/").Plugin()]

    def run(self):
        for plugin in self._plugins:
            plugin.run()

app = Plugin_wrapper(plugins)
app.run()
