import decimal
import json
from pprint import pprint


class DynamoDB:
    def __init__(self, table_name, client=None, region=None, resource=None):
        self.table_name = table_name
        self.dynamodb = resource
        self.region = region
        self.client = client

    def check_if_table_exists(self):
        response = self.client.list_tables()['TableNames']
        print(f'tables: {response}')
        return True if self.table_name in response else False

    def create_db(self):
        exists = self.check_if_table_exists()
        if not exists:
            table = self.client.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'Username',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'Password',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'Username',
                     'AttributeType': 'S'
                     },
                    {
                        'AttributeName': 'Password',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
        else:
            print(f'Table {self.table_name} already exists')

    def get_table(self):
        return self.client.list_tables()['TableNames']

    def drop_table(self):
        response = self.client.delete_table(TableName=self.table_name)
        return pprint(response)