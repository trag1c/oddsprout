import string

BASE_TYPES = frozenset(("any", "array", "object"))
BOUNDS_KEYS = frozenset(
    ("collection", "collection-max", "base", "base-max", "string", "string-max")
)
CATEGORIES = frozenset(("bounds", "types"))
CHARSETS = {
    "ascii": "".join(map(chr, range(128))),
    "alpha": string.ascii_letters,
    "alnum": string.ascii_letters + string.digits,
    "digits": string.digits,
}
VALID_TYPES = frozenset(
    ("int", "float", "number", "string", "boolean", "null", "array", "object")
)
DEFAULT_TYPES = ("int", "float", "string", "boolean", "null", "array", "object")
TYPES_KEYS = frozenset(("charset", "base", "exclude", "include"))
