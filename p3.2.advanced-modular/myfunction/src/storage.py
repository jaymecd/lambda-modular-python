import random
import time


def count_items(path: str, days: int) -> int:
    offset = get_seconds(days)

    record = read_record(path, offset)

    return record["count"]


def get_seconds(days: int) -> int:
    return days * 86400


def read_record(path: str, offset: int) -> dict:
    """
    Simulate load
    """

    print("request throttling, retry in 2 seconds ...")
    time.sleep(2)

    return {
        "path": path,
        "count": random.randint(0, offset),
    }
