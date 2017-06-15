import sys
import boto3
import config
import pprint

from config import args

def create_collection(client, collection_id):
	response = client.create_collection(CollectionId = collection_id)
	return response


def add_face_to_collection(client, source, collection_id, external_image_id):
	with open(source, 'rb') as source_image:
		source_bytes = source_image.read()

	response = client.index_faces(
					CollectionId = collection_id,
					Image = {'Bytes': source_bytes},
					ExternalImageId = external_image_id
	)
	return response

if __name__ == '__main__':
	if not args['user']:
		print("Please provide user argument (for help run: setup.py --help)")
		sys.exit()
	else:
		username = args['user']
		print (username)

		# Setup boto client
		client = boto3.client('rekognition',
		aws_access_key_id=config.get('aws_access_key_id'),
	    aws_secret_access_key=config.get('aws_secret_access_key'),
	    region_name=config.get('aws_region'))

	    # Create a collection for specified user
		response = client.delete_collection(
		CollectionId=username,
		)
		# collection_id = username
		# response = create_collection(rekognition, collection_id)
		# pprint.pprint(response)

