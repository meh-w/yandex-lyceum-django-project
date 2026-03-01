import re
import unicodedata

__all__ = ["normalize_name"]


def normalize_name(name):
    replacements = {
        "a": "а",
        "b": "в",
        "c": "с",
        "e": "е",
        "h": "н",
        "k": "к",
        "m": "м",
        "n": "и",
        "o": "о",
        "p": "р",
        "r": "г",
        "t": "т",
        "u": "и",
        "x": "х",
        "y": "у",
        "0": "о",
        "3": "з",
        "4": "ч",
        "6": "б",
        "8": "в",
        "9": "д",
    }

    if not name:
        return ""

    name = unicodedata.normalize("NFKD", name.lower())
    name = name.replace("ё", "e")
    name = "".join(replacements.get(ch, ch) for ch in name)

    name = re.sub(r"[^a-zа-я0-9\s]", "", name)

    name = re.sub(r"\s+", " ", name).strip()

    return name
