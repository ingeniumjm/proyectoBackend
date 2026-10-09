from datetime import datetime, timezone


def ahora():
    return datetime.now(timezone.utc)
