import hashlib


def __hash_text(text: str) -> str:
    text = f"salty__{text}__text"
    return hashlib.sha512(text.encode("utf-8")).hexdigest()


def try_int(text) -> int:
    try:
        return int(text)
    except ValueError:
        return 0
