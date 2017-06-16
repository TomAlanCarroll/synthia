import base64
import pprint
def recognize_face(image, user):
    with open(image, 'rb') as source_image:
		source_bytes = source_image.read()
	response = client.search_faces_by_image(
		CollectionId = user,
		Image = {'Bytes' : source_bytes}
	)
    pprint.pprint(response)