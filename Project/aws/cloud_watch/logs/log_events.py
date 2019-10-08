import os
import time

from Project.aws.gateways.parameter_store import (_read_parameters_store,
                                                  _put_parameter_to_store, )
from Project.aws.gateways.boto import _client
from Project.run import logger


#  todo logger decorator
#  todo use Redis to store sequence_token
#  todo use Celery to send logs to CloudWatch

class CloudWatchLogger:

    def __init__(self):
        self.client = _client('logs')
        self.user = 'sfigiel'  #  todo os.environ['USERNAME']
        self.env = os.environ["FLASK_ENV"]
        # self.log_group_name = f'/aws/{self.user}/{self.env}/flask'
        self.log_group_name = f'/aws/sfigiel/dev/flask'
        self.log_stream_name = 'app-logs'
        self.sequence_token = _read_parameters_store(param_store_name='sfigiel-sequenceToken')

    def describe_log_groups(self, limit: int = 10, group_name: str = '/aws/sfigiel/'):
        response = self.client.describe_log_groups(
            logGroupNamePrefix=group_name,
            # nextToken='string',
            limit=limit
        )
        logger.info(f'call describe_log_groups() => {response}')
        return response

    def create_log_stream(self):
        response = self.client.create_log_stream(
            logGroupName=self.log_group_name,
            logStreamName=self.log_stream_name
        )
        logger.info(f'call create_log_stream. Log stream: {self.log_stream_name} has been created.Response {response}')

    def create_log_group(self):
        try:
            response = self.client.create_log_group(
                logGroupName=self.log_group_name,
            )
            logger.info(f'call create_log_group(): log group has been created {response}')
        except Exception as e:
            logger.error(f'{e}')

    def put_log_events(self, message: str = ''):
        try:
            sequence_token = _read_parameters_store(param_store_name='sfigiel-sequenceToken')[0]
            response = self.client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[
                    {
                        'timestamp': int(time.time() * 1000),
                        'message': message
                    },
                ],
                sequenceToken=sequence_token
            )
            logger.info(f'call put_log_events().Response: {response}')
            self.sequence_token = response['nextSequenceToken']
            _put_parameter_to_store(value=self.sequence_token)

        except Exception as e:
            logger.error(f'call put_log_events().Error {e}')
            response = self.client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[
                    {
                        'timestamp': int(time.time() * 1000),
                        'message': "init logs"
                    },
                ],
            )
            logger.info(f'call put_log_events().Exception response: {response}')
            self.sequence_token = response['nextSequenceToken']
            _put_parameter_to_store(value=self.sequence_token)

    def __repr__(self):
        return f"Logger([{self.client}, {self.user}, {self.env}, {self.log_group_name}])"

    def __str__(self):
        return f"{self.client}, {self.user}, {self.env}, {self.log_group_name}"
