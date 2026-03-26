__all__ = (
    "generate_b_variants",
    "normalize_name",
)

import re
import unicodedata


def normalize_name(name):
    if not name:
        return ""

    name = unicodedata.normalize("NFKD", name.lower())

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
        "i": "и",
        "l": "и",
        "x": "х",
        "y": "у",
        "0": "о",
        "1": "и",
        "3": "з",
        "4": "ч",
        "6": "б",
        "8": "в",
        "9": "д",
        "ё": "е",
        "й": "и",
    }

    result = []
    for ch in name:
        if ch in replacements:
            result.append(replacements[ch])
        else:
            if re.match(r"[а-я0-9ьъ]", ch):
                result.append(ch)

    return re.sub(r"\s+", " ", "".join(result)).strip()


def generate_b_variants(normalized_name):
    chars = list(normalized_name)
    variants = [chars]

    for i, ch in enumerate(chars):
        if ch == "в":
            new_variants = []
            for var in variants:
                for replacement in ["в", "ь", "ъ"]:
                    tmp = var.copy()
                    tmp[i] = replacement
                    new_variants.append(tmp)

            variants.extend(new_variants)

    return ["".join(v) for v in variants]
