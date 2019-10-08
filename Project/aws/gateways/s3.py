import logging as logger

import boto3
from flask_restful import reqparse

from Project.aws.entities.serializers import serializer
from Project.aws.gateways.session import (_get_s3_resource, )

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('bucket_name', type=str, default=False, required=True)
parser.add_argument('file_name', type=str, default=False, required=False)
parser.add_argument('path', type=str, default=False, required=False)


def get_buckets_list():
    client = boto3.client('s3')
    return client.list_buckets().get('Buckets')


def _list_s3_buckets():
    client = boto3.client('s3')
    response = client.list_buckets()
    if response['Buckets']:
        json_data = serializer(response, filter='Buckets')
        return json_data
    else:
        return {}


def _delete_s3_bucket_files(**kwargs):
    args = parser.parse_args() # {'bucket_name': 'pgs-s3', 'file_name': 'db-settings.txt', 'path': False}
    bucket_name = args['bucket_name']
    file_name = args['file_name']

    s3_resource = _get_s3_resource()

    my_bucket = s3_resource.Bucket(bucket_name)
    try:
        my_bucket.Object(file_name).delete()
    except Exception as e:
        logger(e)
    #
    return {"HTTPStatusCode": 200,
            'action': 'delete',
            'file_name': file_name,
            'bucket_name': bucket_name}


def _upload_s3_bucket_file(bucket_name=None, path=None, file_name=None):
    try:
        args = parser.parse_args()
        bucket_name = args['bucket_name']
        path = args['path']
        file_name = args['file_name']
    except Exception as e:
        print(f'{e}')

    s3_resource = _get_s3_resource()
    try:
        s3_resource.Bucket(bucket_name).upload_file(f'{path}', file_name)
        return {"HTTPStatusCode": 200, 'action': 'upload', 'file_name': file_name, 'bucket_name': bucket_name,
                'path': path}
    except FileNotFoundError:
        return {"FileNotFoundError": f'{file_name} does not exists'}


def _download_s3_bucket_file():
    args = parser.parse_args()
    bucket_name = args['bucket_name']
    file_name = args['file_name']
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, file_name, file_name)
        return {"HTTPStatusCode": 200, 'file_name': file_name, 'bucket_name': bucket_name}
    except:
        json_data = _list_s3_bucket_files()
        if bucket_name not in {el['Key'] for el in json_data.values()}:
            return {"HTTPStatusCode": 200,
                    'info': f'{file_name} does not exists in S3 bucket: {bucket_name}',
                    bucket_name: json_data}


def _list_s3_bucket_files(bucket_name=None):
    if not bucket_name: ##todo
        args = parser.parse_args()
        bucket_name = args['bucket_name']

    s3 = boto3.client('s3')
    bucket = s3.list_objects(Bucket=bucket_name)
    if bucket:
        json_data = serializer(bucket['Contents'])
        return json_data
    else:
        return bucket