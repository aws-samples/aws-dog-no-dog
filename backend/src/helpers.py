import copy
import json
import os


DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "*")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")


def response(message, status_code=200):
    """
    Return a properly formatted response for AWS Lambda proxy integration
    including CORS
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
            "Access-Control-Allow-Origin": "{}".format(DOMAIN_NAME),
            "Access-Control-Allow-Methods": "POST,GET,OPTIONS"
        },
        "body": json.dumps(message)
    }


def metric(namespace, metric_name, metric_value, metric_unit="None", dimensions={}):
    # Always inject 'Environment' as a dimension
    dimensions = copy.deepcopy(dimensions)
    dimensions["Environment"] = ENVIRONMENT

    print("MONITORING|{value}|{unit}|{name}|{namespace}|{dimensions}".format(
        value=metric_value,
        unit=metric_unit,
        name=metric_name,
        namespace=namespace,
        dimensions=",".join(["{}={}".format(k, v) for k, v in dimensions.items()])
    ))
