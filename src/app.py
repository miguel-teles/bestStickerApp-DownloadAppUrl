import os

import boto3
from utils import *

BUCKET_NAME = os.environ['BUCKET_NAME']

def generate_download_url(version_name):
    key = version_name + "/app-release.apk"

    presigned_url = boto3.client('s3').generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': key},
        ExpiresIn=120
    )

    return {
        'presignedUrl': presigned_url
    }

def lambda_handler(event, context):
    try:
        body = event.get('body')
        if body is None:
            raise ValueError("Request body is required")
        version_name = json.loads(body).get('versionName')
        if version_name is None:
            raise ValueError("Version name is required")

        return respondSuccess(generate_download_url(version_name))
    except ValueError as ex:
        return respondError(400, str(ex))
    except Exception as ex:
        return respondError(500, str(ex))