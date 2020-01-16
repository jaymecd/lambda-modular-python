import os

from .stats import generate_summary

RECORD_PATH = os.environ.get('X_PATH', 's3://sample/path')


def lambda_handler(event: dict, context):
    # set default
    event.setdefault('days', 3)

    return generate_summary(RECORD_PATH, event['days'])
