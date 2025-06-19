import json
import os
import inspect
from functools import wraps
from modules.settings import settings

ENABLED = settings["dev"]["api_cache"]

# Ensure the cache folder exists
CACHE_FOLDER = "cache"
os.makedirs(CACHE_FOLDER, exist_ok=True)


def cache(func):
    # Get module or filename which are usually the same
    module_name = (
        func.__module__
        if func.__module__ != "__main__"
        else os.path.basename(inspect.stack()[1].filename).replace(".py", "")
    )

    # Cache file path
    cache_file = os.path.join(CACHE_FOLDER, f"{module_name}_{func.__name__}_cache.json")

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if cache file exists
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                cache_data = json.load(f)
        else:
            cache_data = {}

        # Unique key for arguments
        key = json.dumps((args, kwargs))

        # Return cached result if available
        if key in cache_data and ENABLED:
            print(f"Returning cached result for {func.__name__}")
            return cache_data[key]

        # Call the function and cache the result
        result = func(*args, **kwargs)
        cache_data[key] = result
        with open(cache_file, "w") as f:
            json.dump(cache_data, f, indent=4)

        return result

    return wrapper
