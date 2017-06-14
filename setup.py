import boto3
import config

rekognition = boto3.client(
	'rekognition',
	aws_access_key_id=config.get('aws_access_key_id'),
    aws_secret_access_key=config.get('aws_secret_access_key')
	)

