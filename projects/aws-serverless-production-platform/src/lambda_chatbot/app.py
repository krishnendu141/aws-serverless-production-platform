#!/usr/bin/env python3
import json
import os
import boto3
from botocore.exceptions import ClientError

# Example chatbot lambda that receives messages via API Gateway and orchestrates RAG call to Bedrock.

bedrock = boto3.client('bedrock-runtime') if boto3.utils else None
s3 = boto3.client('s3')

def handler(event, context):
    # event is API Gateway proxy
    body = {}
    try:
        body = json.loads(event.get('body') or '{}')
    except Exception:
        pass

    query = body.get('query') or 'Hello'

    # Placeholder: retrieve documents from S3 or vector DB
    # For production replace with proper retrieval & vector search
    docs = ["This is a sample document used for RAG."]

    # Build prompt
    prompt = f"You are an assistant. Use these documents: {docs}\nUser Query: {query}"

    # Call Bedrock (this code assumes Bedrock runtime client is available)
    try:
        response = boto3.client('bedrock-runtime').invoke_model(
            modelId=os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-v1'),
            body=json.dumps({
                'input': prompt
            }),
            contentType='application/json'
        )
        payload = response['body'].read().decode('utf-8')
    except Exception as e:
        # In many accounts Bedrock isn't enabled; fallback to a mock reply
        payload = json.dumps({"reply": f"[mocked-bedrock] got query: {query}"})

    # return API Gateway proxy response
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'query': query, 'reply': payload})
    }
