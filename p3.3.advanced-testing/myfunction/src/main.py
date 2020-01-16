import json
import os

import boto3
import logging

from . import services

_logger = logging.getLogger()
_logger.setLevel(logging.INFO)

X_CODE = os.environ.get("X_CODE", 'testing')
X_NS_DICT = json.loads(os.environ.get("X_NS_DICT", '{"org": "org.corporate", "com": "com.company"}'))


def lambda_handler(event, context):
    event.setdefault('ns', 'org')

    _logger.info(f"handle_request, event={event}")

    try:
        return services.build_result(context, event['ns'], X_NS_DICT, X_CODE)
    except RuntimeError as ex:
        return {
            "error": str(ex),
        }
