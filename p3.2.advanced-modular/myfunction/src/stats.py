import datetime
import platform

import markdown2

from .storage import count_items


def generate_summary(path: str, days: int) -> dict:
    now = datetime.datetime.utcnow()

    return {
        "storage": count_items(path, days),
        "python": platform.python_version(),
        "markdown2": markdown2.__version__,
        "time": now.isoformat(),
    }
