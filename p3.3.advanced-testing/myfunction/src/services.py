import json
import logging
import time
from typing import Callable, Generator, List, Mapping

import boto3
import yaml

_logger = logging.getLogger(__name__)
_session = boto3.Session(region_name='eu-west-1')


def request_status(context, namespace: str, code: str):
    _logger.info(f"run request_status")

    client = _session.client('ssm')

    for i in range(0, 2):
        if i == 2:
            break

        # client  # mimic load with delay
        _logger.warning(f"got throttling exception, sleep 3 second before retry ...")
        time.sleep(3)

    status = f"{namespace}:{_sanitize_code(code)}/{context.aws_request_id}"

    return status

def _sanitize_code(code: str):
    return code.upper()


def build_result(context, key: str, namespaces: dict, code: str):
    _logger.info(f"run build_result")

    try:
        namespace = namespaces[key]
    except KeyError as ex:
        raise RuntimeError(f"Key '{key}' is not defined") from ex

    result = request_status(context, namespace, code)

    return {
        'result': result,
        'yaml': yaml.__version__,
    }
