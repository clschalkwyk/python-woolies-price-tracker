import os
from os.path import dirname, abspath
from uuid import uuid4
import glob
import json

import boto3 as boto3
from dotenv import load_dotenv

path = dirname(abspath(__file__)) + '/.env'
load_dotenv(path)

dynamodb = boto3.resource('dynamodb')
db_client = boto3.client('dynamodb')
_table = dynamodb.Table(os.getenv('TABLE_NAME'))

for file in glob.glob('./*.json'):
    date = file.split('.')[1].split('_')[1::1]
    date = f'{date[0][0:4]}-{date[0][4:6]}-{date[0][6:8]} {date[1][0:2]}:{date[1][2:4]}:{date[1][4:6]}'
    dat = json.load(open(file,'r'))
    for x in dat:
        x.update({
            'Pk': uuid4().__str__(),
            'datasource': 'woolies',
            'date': date
        })
        x.update({
            'unitPrice': str(x['unitPrice']),
            'price':  str(x['price']),
        })
        _table.put_item(Item=x)

print('-done-')

