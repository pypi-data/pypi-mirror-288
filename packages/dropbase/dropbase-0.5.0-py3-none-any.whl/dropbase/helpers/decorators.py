import inspect
from functools import wraps


def clear_store_add(func):
    @wraps(func)
    def wrapper(self, state, context, store, *args, **kwargs):
        try:
            result = func(self, state, context, store, *args, **kwargs)
            table_name = self.__class__.__name__.lower()
            method_name = func.__name__
            store = result[1]
            if hasattr(store, table_name) and hasattr(getattr(store, table_name), method_name):
                target_section = getattr(getattr(store, table_name), "add")
                clear_add_attributes(target_section)
            result = result[0], store
            return result
        except Exception as e:
            raise e

    return wrapper


def clear_add_attributes(obj):
    """Clear attributes of the given object"""
    for attr_name, attr_value in inspect.getmembers(obj):
        # Skip callable methods and dunder attributes
        if attr_name in (
            "_abc_impl",
            "_abc_registry",
            "_abc_cache",
            "_abc_negative_cache_version",
            "_abc_invalidation_counter",
        ):
            continue
        if not (attr_name.startswith("__") and attr_name.endswith("__")) and not callable(attr_value):
            if isinstance(attr_value, list):
                obj.__setattr__(attr_name, [])
            elif isinstance(attr_value, dict):
                obj.__setattr__(attr_name, {})
            elif hasattr(attr_value, "__dict__"):
                clear_add_attributes(attr_value)  # Recursively clear nested objects
            else:
                obj.__setattr__(attr_name, None)


def clear_store_update(func):
    @wraps(func)
    def wrapper(self, state, context, store, *args, **kwargs):
        try:
            result = func(self, state, context, store, *args, **kwargs)
            table_name = self.__class__.__name__.lower()
            store = result[1]
            if hasattr(store, table_name) and hasattr(getattr(store, table_name), "update"):
                store.__getattribute__(table_name).__setattr__("update", [])
            result = result[0], store
            return result
        except Exception as e:
            raise e

    return wrapper


def clear_update_attributes(obj, attr_name=None):
    attr_value = getattr(obj, attr_name)
    if isinstance(attr_value, list):
        obj.__setattr__(attr_name, [])
    else:
        obj.__setattr__(attr_name, None)
