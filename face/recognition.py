import base64
import pprint
import boto3
import config
from PIL import Image

client = boto3.client('rekognition',
	aws_access_key_id=config.get('aws_access_key_id'),
	aws_secret_access_key=config.get('aws_secret_access_key'),
	region_name=config.get('aws_region')
)

def get_username_from_image(image):
	im = Image.fromarray(image)
	im.save('rekognition.jpg', 'JPEG')

	with open('rekognition.jpg', 'rb') as source_image:
		source_bytes = source_image.read()

	response = client.search_faces_by_image(
		CollectionId = 'Synthia',
		Image = {'Bytes' : source_bytes}
	)

	if response['FaceMatches']:
		return response['FaceMatches'][0]['Face']['ExternalImageId']
	else:
		return None

