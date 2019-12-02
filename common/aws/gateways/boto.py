import boto3

from common.logger import *


def _client(region_name: str, service: str):
    logger.info(f'call _client(service={service}, region_name={region_name})')
    return boto3.client(service, region_name)


def _get_cloud_watch_logs(log_group: str):
    client = _client('logs')
    response = client.filter_log_events(logGroupName=log_group, limit=10000)
    return response


def _get_s3_resource():
        return boto3.resource('s3')
