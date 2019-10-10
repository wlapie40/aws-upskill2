from flask_restful import Resource

from Project.aws.gateways.s3 import (
    _list_s3_buckets,
    _delete_s3_bucket_files,
    _upload_s3_bucket_file,
    _download_s3_bucket_file,
    _list_s3_bucket_files,
)


class ListS3Buckets(Resource):
    def get(self):
        return _list_s3_buckets()


class ListS3BucketFiles(Resource):
    def get(self):
        return _list_s3_bucket_files()


class DeleteS3BucketFile(Resource):
    def get(self):
        return _delete_s3_bucket_files()


class DownloadS3BucketFile(Resource):
    def get(self):
        return _download_s3_bucket_file()


class UploadS3BucketFile(Resource):
    def post(self):
        return _upload_s3_bucket_file()
