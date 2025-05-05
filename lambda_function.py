import boto3
import os
import uuid
import json
from PIL import Image

s3_client = boto3.client('s3')

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((128, 128))
        image.save(resized_path)

def lambda_handler(event, context):
    for record in event['Records']:
        message_body = json.loads(record['body'])
        
        s3_event = json.loads(message_body['Message'])
        
        s3_records = s3_event['Records'] if 'Records' in s3_event else [s3_event]
        
        for s3_record in s3_records:
            bucket = s3_record['s3']['bucket']['name']
            key = s3_record['s3']['object']['key']
            
            download_path = f'/tmp/{uuid.uuid4()}-{os.path.basename(key)}'
            upload_path = f'/tmp/resized-{os.path.basename(key)}'
            
            s3_client.download_file(bucket, key, download_path)
            resize_image(download_path, upload_path)
            s3_client.upload_file(upload_path, os.environ['OUTPUT_BUCKET'], f'resized-{os.path.basename(key)}')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }