import base64
import binascii
import json
import os
import uuid
import helpers
import boto3


BUCKET_NAME = os.environ.get("BUCKET_NAME", "")


rekognition = boto3.client("rekognition")
s3 = boto3.client("s3")


def has_dog(photo):
    labels = rekognition.detect_labels(
        Image={
            "Bytes": photo
        },
        MinConfidence=90
    )

    for label in labels.get("Labels", []):
        if label["Name"].lower() == "dog":
            return True

    return False


def save_feedback(photo, user_dog, system_dog):
    s3.put_object(
        Body=photo,
        Bucket=BUCKET_NAME,
        Key=str(uuid.uuid4()),
        Metadata={
            "user_dog": str(user_dog).lower(),
            "system_dog": str(system_dog).lower()
        }
    )


def has_dog_handler(event, _):
    # Try to decode a JSON document from the body
    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError:
        return helpers.message({"message": "Invalid JSON document"}, 400)

    # Validate the JSON document
    if "photo" not in body:
        return helpers.message({"message": "Missing 'photo' key in body"}, 400)

    # Try to extract the photo from the JSON document
    try:
        photo = base64.b64decode(body["photo"])
    except binascii.Error:
        return helpers.message({"message": "Invalid base64 string for 'photo'"}, 400)

    # Check if there is a dog
    dog = has_dog(photo)

    # Store if there was a dog or not as a custom metric
    helpers.metric("DogNoDog", "Dog", int(dog))

    return helpers.response({"dog": dog})


def feedback_handler(event, _):
    # Try to decode a JSON document from the body
    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError:
        return helpers.message({"message": "Invalid JSON document"}, 400)

    # Validate the JSON document
    if "photo" not in body:
        return helpers.message({"message": "Missing 'photo' key in body"}, 400)

    if "dog" not in body:
        return helpers.message({"message": "Missing 'dog' key in body"}, 400)

    user_dog = body["dog"]

    # Try to extract the photo from the JSON document
    try:
        photo = base64.b64decode(body["photo"])
    except binascii.Error:
        return helpers.message({"message": "Invalid base64 string for 'photo'"}, 400)

    # Check if the system finds a dog
    dog = has_dog(photo)

    # Store if there was a dog or not as a custom metric
    helpers.metric("DogNoDog", "Dog", int(dog))

    # Store the type of error as a custom metric.
    # FalsePositive: there are no dogs in the picture but the system detected one.
    # FalseNegative: there is a dog in the picture but the system did not detect it.
    # Match: the system correctly detected that there is a dog.
    if dog and not user_dog:
        helpers.metric("DogNoDog", "FalsePositive", 1)
    elif not dog and user_dog:
        helpers.metric("DogNoDog", "FalseNegative", 1)
    else:
        helpers.metric("DogNoDog", "Match", 1)

    # Store the feedback on S3
    save_feedback(photo, user_dog, dog)

    # Send message back to the user
    return helpers.response({"message": "Feedback received"})
