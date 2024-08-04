from datetime import datetime


def is_naive(date: datetime) -> bool:
    """Checks if the given datetime is naive."""
    return date.tzinfo is None or date.tzinfo.utcoffset(date) is None
