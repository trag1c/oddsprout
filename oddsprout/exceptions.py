class OddsproutError(Exception):
    """Base class for Oddsprout errors."""


class OddsproutConfigurationError(OddsproutError):
    """Exception for errors found in the configuration file."""


class OddsproutValueError(OddsproutError, ValueError):
    """Exception for errors related to incorrect values provided to `generate_json`."""
