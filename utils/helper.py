import collections.abc

def str_limit(s, max, suffix='..'):
    return (s[:max] + suffix) if len(s) > max else s

def deep_update(source: dict, overrides: dict) -> dict:
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    Source: https://stackoverflow.com/a/30655448/1862500
    """
    for key, value in overrides.items():
        if isinstance(value, collections.abc.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source