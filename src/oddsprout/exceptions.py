class OddsproutError(Exception):
    """Base class for oddsprout errors."""


class OddsproutConfigurationError(OddsproutError):
    """Exception for errors found in the configuration file."""


class OddsproutValueError(OddsproutError, ValueError):
    """Exception for incorrect values provided to oddsprout objects."""


class OddsproutRecursionError(OddsproutError, RecursionError):
    """Exception for errors related to recursion limits caused by oddsprout."""
