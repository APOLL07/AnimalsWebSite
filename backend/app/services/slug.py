"""Slug generation utility."""

import re
import uuid

from sqlalchemy.orm import Session

from app.models.product import Product

_TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def _transliterate(text: str) -> str:
    result = []
    for ch in text.lower():
        result.append(_TRANSLIT.get(ch, ch))
    return "".join(result)


def generate_slug(name: str, db: Session) -> str:
    base = _transliterate(name)
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    if not base:
        base = "product"

    slug = base
    counter = 1
    while db.query(Product).filter(Product.slug == slug).first():
        slug = f"{base}-{counter}"
        counter += 1
    return slug
