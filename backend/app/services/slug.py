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

# Russian/Ukrainian animal names → English translation for slug generation
_ANIMAL_TRANSLATIONS: dict[str, str] = {
    # Common pets
    "кіт": "cat", "кот": "cat", "кішка": "cat", "кошка": "cat",
    "собака": "dog", "пес": "dog", "пёс": "dog",
    "кролик": "rabbit", "кріль": "rabbit",
    "хом'як": "hamster", "хомяк": "hamster",
    "морська свинка": "guinea-pig", "морская свинка": "guinea-pig",
    "папуга": "parrot", "попугай": "parrot",
    "черепаха": "turtle",
    "риба": "fish", "рыба": "fish",
    "щур": "rat", "крыса": "rat",
    "миша": "mouse", "мышь": "mouse",
    "їжак": "hedgehog", "ёж": "hedgehog", "їжачок": "hedgehog",
    "тхір": "ferret", "хорек": "ferret",
    "шиншила": "chinchilla",
    "дегу": "degu",
    "гербіл": "gerbil", "песчанка": "gerbil",
    "ящірка": "lizard", "ящерица": "lizard",
    "змія": "snake", "змея": "snake",
    "хамелеон": "chameleon",
    "геко": "gecko",
    "пацюк": "rat",
    # Farm / large animals
    "кінь": "horse", "конь": "horse", "кобила": "horse",
    "корова": "cow", "бик": "bull",
    "свиня": "pig", "свинья": "pig",
    "вівця": "sheep", "овца": "sheep",
    "коза": "goat",
    "курка": "chicken", "курица": "chicken", "півень": "rooster", "петух": "rooster",
    "качка": "duck", "утка": "duck",
    "гуска": "goose", "гусь": "goose",
    "індик": "turkey", "индюк": "turkey",
    "кролі": "rabbits",
    # Wild / exotic
    "лев": "lion",
    "тигр": "tiger",
    "ведмідь": "bear", "медведь": "bear",
    "вовк": "wolf", "волк": "wolf",
    "лисиця": "fox", "лиса": "fox",
    "заєць": "hare", "заяц": "hare",
    "олень": "deer",
    "лось": "moose",
    "кабан": "boar",
    "мавпа": "monkey", "обезьяна": "monkey",
    "слон": "elephant",
    "жираф": "giraffe",
    "зебра": "zebra",
    "носоріг": "rhinoceros", "носорог": "rhinoceros",
    "бегемот": "hippopotamus",
    "крокодил": "crocodile",
    "орел": "eagle",
    "сова": "owl",
    "папуга": "parrot",
    "пінгвін": "penguin", "пингвин": "penguin",
    "фламінго": "flamingo", "фламинго": "flamingo",
    "дельфін": "dolphin", "дельфин": "dolphin",
    "акула": "shark",
    "кит": "whale",
    "восьминіг": "octopus", "осьминог": "octopus",
    "краб": "crab",
    "омар": "lobster",
    "медуза": "jellyfish",
}


def translate_animal_name(name: str) -> str:
    """Translate animal name from Russian/Ukrainian to English for slug.
    Falls back to transliteration if no translation found."""
    key = name.strip().lower()
    if key in _ANIMAL_TRANSLATIONS:
        return _ANIMAL_TRANSLATIONS[key]
    return _transliterate(name)


def _transliterate(text: str) -> str:
    result = []
    for ch in text.lower():
        result.append(_TRANSLIT.get(ch, ch))
    return "".join(result)


def generate_slug(name: str | dict, db: Session) -> str:
    if isinstance(name, dict):
        name = name.get("ru") or name.get("uk") or "product"
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
