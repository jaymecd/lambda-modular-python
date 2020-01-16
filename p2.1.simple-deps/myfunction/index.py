import datetime
import platform

import yaml


def lambda_handler(event, context):
    result = {
        "python": platform.python_version(),
        "yaml": yaml.__version__,
        "time": datetime.datetime.utcnow().isoformat(),
    }

    return result
