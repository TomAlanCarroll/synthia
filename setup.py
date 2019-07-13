import sys
import os
import boto3
import config
import pprint
import time
import picamera

from config import args
from ConfigParser import SafeConfigParser


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


def add_username_to_config_ini(username):
    config = SafeConfigParser()
    config.read('config.ini')

    if not config.has_section('main'): 
        config.add_section('main')
        config.set('main', 'users', username)
    else:
        users = config.get('main', 'users')

        user_already_in_config = False
        for user in users.split(','):
            if user == username:
                user_already_in_config = True
                break

        if user_already_in_config is False:
            config.set('main', 'users', users + ',' + username)

    with open('config.ini', 'w') as f:
        config.write(f)


def synthesize_polly_clips(client, username):
    if not os.path.exists('clips'):
        os.makedirs('clips')
    # Synthesize welcome home message
    resp = client.synthesize_speech(OutputFormat='mp3',
        Text='Welcome home ' + username,
        VoiceId=config.get('aws_polly_voice'))
    with open('clips/Welcome_' + username + '.mp3', 'wb') as f:
        f.write(resp['AudioStream'].read())


def test_face_collection(client, source, collection_id):
    with open(source, 'rb') as source_image:
        source_bytes = source_image.read()

    response = client.search_faces_by_image(
        CollectionId = collection_id,
        Image = {'Bytes' : source_bytes}
    )
    return response


if __name__ == '__main__':
    if not args['user']:
        print("Please provide user argument (for help run: setup.py --help)")
        sys.exit()

    username = args['user']
    print(username)

    add_username_to_config_ini(username)

    polly_client = boto3.client('polly',
                          aws_access_key_id=config.get('aws_access_key_id'),
                          aws_secret_access_key=config.get('aws_secret_access_key'),
                          region_name=config.get('aws_region')
                          )

    synthesize_polly_clips(polly_client, username)
    sys.exit()
    # Setup boto client
    rekognition_client = boto3.client('rekognition',
                          aws_access_key_id=config.get('aws_access_key_id'),
                          aws_secret_access_key=config.get('aws_secret_access_key'),
                          region_name=config.get('aws_region')
                          )
    # To clear out the collection
    # response = rekognition_client.delete_collection(
    # CollectionId=username
    # )
    # sys.exit()
    create_collection_if_needed(rekognition_client, username)

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
        response = add_face_to_collection(rekognition_client, capture_filename, 'Synthia', 'Tom')
        pprint.pprint(response)

        # Test the image by searching for another
        print('Testing search in 1 ...')
        time.sleep(1)
        capture_test_filename = username + '_test.jpg'
        camera.capture(capture_test_filename)
        response = test_face_collection(rekognition_client, capture_test_filename, username)
        pprint.pprint(response)
