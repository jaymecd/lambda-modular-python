import json
import os

from .ioc import get_container

init_error = None

try:
    container = get_container(
        code=os.environ.get("X_CODE", 'testing'),
        ns_dict=json.loads(os.environ.get("X_NS_DICT", '{"org": "org.corporate", "com": "com.company"}')),
    )
except Exception as ex:
    init_error = ex


def lambda_handler(event, context):
    if init_error:
        raise init_error

    container.context.use(context)

    return container.direct_handler(event)
