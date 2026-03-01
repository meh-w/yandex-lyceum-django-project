__all__ = ["str_to_bool_allow_reverse"]


def str_to_bool_allow_reverse(value):
    if value is None:
        return True
    return value in {"", "true", "True", "yes", "YES", "1", "y"}
