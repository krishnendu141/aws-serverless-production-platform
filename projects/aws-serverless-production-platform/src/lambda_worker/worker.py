#!/usr/bin/env python3
import json
import os
import boto3

sqs = boto3.client('sqs')

def handler(event, context):
    # Worker to process SQS messages
    print('Worker event:', event)
    for record in event.get('Records', []):
        body = record.get('body')
        print('Processing message:', body)
    return {'status': 'ok'}
