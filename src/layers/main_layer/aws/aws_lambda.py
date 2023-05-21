import json

import boto3

lambda_client = boto3.client("lambda")


def invoke(func_identifier: str, event: dict, invocation_type="Event"):
    return lambda_client.invoke(
        FunctionName=func_identifier,
        InvocationType=invocation_type,
        Payload=json.dumps(event).encode(),
    )
