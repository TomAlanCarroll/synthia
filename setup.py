import sys
import boto3
import config
import pprint
import time
import picamera

from config import args

def create_collection_if_needed(client, username):
    # Check if user already exists
    response = client.list_collections()

    if username in response['CollectionIds']:
        print(username + ' already has a collection; skipping create')
    else:
        # Create a collection for specified user
        collection_id = username
        response = create_collection(client, collection_id)
        print('Created collection with ID ' + username)

def create_collection(client, collection_id):
    response = client.create_collection(CollectionId=collection_id)
    return response


def add_face_to_collection(client, source, collection_id, external_image_id):
    with open(source, 'rb') as source_image:
        source_bytes = source_image.read()

    response = client.index_faces(
        CollectionId=collection_id,
        Image={'Bytes': source_bytes},
        ExternalImageId=external_image_id
    )
    return response


if __name__ == '__main__':
    if not args['user']:
        print("Please provide user argument (for help run: setup.py --help)")
        sys.exit()

    username = args['user']
    print (username)

    # Setup boto client
    client = boto3.client('rekognition',
                          aws_access_key_id=config.get('aws_access_key_id'),
                          aws_secret_access_key=config.get('aws_secret_access_key'),
                          region_name=config.get('aws_region')
                          )
    # To clear out the collection
    # response = client.delete_collection(
    # CollectionId=username,
    # )
    # sys.exit()
    create_collection_if_needed(client, username)

    # Snap a photo to add to the collection for the user
    with picamera.PiCamera() as camera:
        camera.resolution = tuple(config.get("resolution"))
        camera.start_preview()
        # Notify a photo will be taking (minimum camera warmup time is around 2 seconds)
        print('Taking a photo in 3 ...')
        time.sleep(1)
        print('                  2 ...')
        time.sleep(1)
        print('                  1 ...')
        time.sleep(1)

        capture_filename = username + '.jpg'
        camera.capture(capture_filename)
        response = add_face_to_collection(client, capture_filename, username, capture_filename)
        pprint.pprint(response)
