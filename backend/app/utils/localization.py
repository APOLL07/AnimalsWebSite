SUPPORTED_LANGUAGES = ("uk", "ru")
DEFAULT_LANGUAGE = "uk"


def get_localized(value, lang: str) -> str:
    """Extract a localized string from a JSONB dict, with fallback."""
    if isinstance(value, dict):
        return value.get(lang) or value.get(DEFAULT_LANGUAGE) or ""
    return value or ""
