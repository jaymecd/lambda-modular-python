import json
import logging
import time
from typing import Callable, Generator, List, Mapping

import boto3
import yaml

from .di import LambdaContext

_logger = logging.getLogger(__name__)


def status_requester(session: boto3.Session, context: LambdaContext, code: str) -> Callable:
    """ service factory """
    def closure(namespace: str):
        """ service instance """
        _logger.info(f"run svc:status_requester")

        client = session.client('ssm')

        for i in range(0, 2):
            if i == 2:
                break

            # client  # mimic load with delay
            _logger.warning(f"got throttling exception, sleep 3 second before retry ...")
            time.sleep(3)

        status = f"{namespace}:{_sanitize_code(code)}/{context.aws_request_id}"
        return status

    return closure


def _sanitize_code(code: str):
    return code.upper()


def result_builder(request_status: status_requester, ns_dict: dict) -> Callable:
    """ service factory """
    def closure(key: str):
        """ service instance """
        _logger.info(f"run svc:result_builder")

        try:
            namespace = ns_dict[key]
        except KeyError as ex:
            raise RuntimeError(f"Key '{key}' is not defined") from ex

        result = request_status(namespace)

        return {
            'result': result,
            'yaml': yaml.__version__,
        }

    return closure


def direct_handler(build_result: result_builder) -> Callable:
    """ service factory """
    def closure(event: dict):
        """ service instance """
        event.setdefault('key', 'org')

        _logger.info(f"handle_request, event={event}")

        try:
            return build_result(event['key'])
        except RuntimeError as ex:
            return {
                "error": str(ex),
            }

    return closure
