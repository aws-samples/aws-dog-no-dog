import copy
import json
import os
import time


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
    """
    Generate custom metrics

    This works by printing into a specific JSON format documented here:
    https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html
    """

    retval = copy.deepcopy(dimensions)
    # Always inject 'Environment' as a dimension
    retval["Environment"] = ENVIRONMENT

    # Inject the embedded metric for CloudWatch
    # See https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format.html
    retval["_aws"] = {
        "CloudWatchMetrics": [{
            "Namespace": namespace,
            "Dimensions": [list(retval.keys())],
            "Metrics": [{
                "Name": metric_name,
                "Unit": metric_unit
            }]
        }],
        "Timestamp": int(time.time()*1000)
    }

    # Inject the metric value in the JSON blob
    retval[metric_name] = metric_value

    print(json.dumps(retval))
