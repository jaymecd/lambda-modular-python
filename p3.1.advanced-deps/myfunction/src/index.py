import datetime
import platform

import markdown2
import natsort
import yaml


def lambda_handler(event, context):
    result = {
        "python": platform.python_version(),
        "yaml": yaml.__version__,
        "markdown2": markdown2.__version__,
        "natsort": natsort.__version__,
        "time": datetime.datetime.utcnow().isoformat(),
    }

    return result
