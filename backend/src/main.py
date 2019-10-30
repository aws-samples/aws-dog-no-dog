import json
import os


DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "*")


def response(message, status_code=200):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
            "Access-Control-Allow-Origin": "{}".format(DOMAIN_NAME),
            "Access-Control-Allow-Methods": "POST,GET,OPTIONS"
        },
        "body": json.dumps(message)
    }


def has_dog_handler(event, _):
    pass
