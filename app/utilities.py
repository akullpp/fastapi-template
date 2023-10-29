from functools import reduce
from typing import Any


def safe_get(dictionary: dict, keys: str, default:Any=None) -> Any | None:
    """Safely gets a value from a dictionary using a dot-separated string of keys."""
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


def add(dictionary: dict, item: tuple[str, Any]) -> dict:
    """Adds a key-value pair to a dictionary inplace if the value is not None."""
    key, value = item
    if value is not None:
        dictionary[key] = value


def add_all(dictionary: dict, items: list[tuple[str, Any]]) -> dict:
    """Adds multiple key-value pairs to a dictionary inplace if the value is not None."""
    for item in items:
        add(dictionary, item)
    return dictionary
