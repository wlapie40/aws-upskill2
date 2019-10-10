import boto3
from flask import session

from Project.aws.gateways.boto import _get_s3_resource


def get_bucket():
    s3_resource = _get_s3_resource()
    if 'bucket' in session:
        bucket = session['bucket']
    return s3_resource.Bucket(bucket)


def get_region_name():
    session = _set_session()
    return session.region_name


def _set_session():
    return boto3.session.Session()