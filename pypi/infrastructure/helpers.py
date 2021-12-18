import hashlib

from pypi.config import get_settings


def __hash_text(text: str) -> str:
    salty = get_settings().salt
    text = f"{salty}__{text}__text"
    return hashlib.sha512(text.encode("utf-8")).hexdigest()


def try_int(text) -> int:
    try:
        return int(text)
    except ValueError:
        return 0
