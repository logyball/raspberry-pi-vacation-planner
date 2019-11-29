from yaml import load
from functools import lru_cache

CONFIG_FILE_PATH = 'config.yaml'


def get_width():
    return _get_config().get('screen_size', {}).get('width', 480)


def get_height():
    return _get_config().get('screen_size', {}).get('height', 800)


@lru_cache(maxsize=4)
def _get_config():
    with open(CONFIG_FILE_PATH) as c_file:
        config_dict = load(c_file.read())
    return config_dict
