import datetime
import json
import platform


def lambda_handler(event, context):
    result = {
        "time": datetime.datetime.utcnow().isoformat(),
        "python": platform.python_version(),
    }

    return json.dumps(result)
