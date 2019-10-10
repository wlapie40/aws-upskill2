import logging as logger

import boto3


def _client(service: str, region_name: str = 'eu-west-1'):
    logger.info(f'call _client(service={service}, region_name={region_name})')
    return boto3.client(service, region_name)


def _get_cloud_watch_logs(log_group: str):
    client = _client('logs')
    response = client.filter_log_events(logGroupName=log_group, limit=10000)
    return response


def _get_s3_resource():
        return boto3.resource('s3')





