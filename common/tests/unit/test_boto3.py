import boto3
import os
from moto import mock_s3

MY_BUCKET = "test-pgs-s3"
PATH = os.path.abspath(r"tests/file_to_upload/clara_db_pass.txt")
FILE_NAME = 'test_clara_db_pass.txt'

# def test_create_bucket():
#     with mock_s3():
#         s3_resource = boto3.resource(
#              "s3",
#              region_name="eu-west-1",
#              aws_access_key_id="fake_access_key",
#              aws_secret_access_key="fake_secret_key",
#          )
#         s3_resource.create_bucket(Bucket=MY_BUCKET)
#         assert _list_s3_buckets()['1']['Name'] == MY_BUCKET

def test_upload_file():
    with mock_s3():
        s3_resource = boto3.resource(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )
        s3_resource.create_bucket(Bucket=MY_BUCKET)

        s3_resource.Bucket(MY_BUCKET).upload_file(PATH, FILE_NAME)
        # s3_client = boto3.client('s3')
        # s3_client.upload_file(PATH, MY_BUCKET, FILE_NAME)
        #
        # assert _list_s3_bucket_files(MY_BUCKET)['1']['Key'] == FILE_NAME

# def test_delete_file():
#     with mock_s3():
#         s3_resource = boto3.resource(
#             "s3",
#             region_name="eu-west-1",
#             aws_access_key_id="fake_access_key",
#             aws_secret_access_key="fake_secret_key",
#         )
#         s3_resource.create_bucket(Bucket=MY_BUCKET)
#
#         s3_client = boto3.client('s3')
#         s3_client.upload_file(PATH, MY_BUCKET, FILE_NAME)
        # _delete_s3_bucket_files(bucket_name = MY_BUCKET, file_name = FILE_NAME)

# def test_download_file():
#     with mock_s3():
#         s3_resource = boto3.resource(
#             "s3",
#             region_name="eu-west-1",
#             aws_access_key_id="fake_access_key",
#             aws_secret_access_key="fake_secret_key",
#         )
#         s3_resource.create_bucket(Bucket=MY_BUCKET)
#
#         s3_client = boto3.client('s3')
#         s3_client.upload_file(PATH, MY_BUCKET, FILE_NAME)



