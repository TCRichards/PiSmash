# export GOOGLE_APPLICATION_CREDENTIALS=kyourcredentials.json
import io
import cv2
import os
import numpy as np
from PIL import Image, ImageDraw
# Imports the Google Cloud client library
from google.cloud import vision

# Explicitly add google credentials to the command line if not there already
curDir = os.getcwd() + '/'
imagePath = curDir + 'selectScreens/screen3.jpg'
credentialsPath = curDir + 'Pi Smash-ecdcebce34a8.json'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentialsPath

# Instantiates a client
client = vision.ImageAnnotatorClient()


def detect_text_vision(path, printing=False):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    labels = np.array([])
    bounds = []
    # print('Texts:')

    for text in texts:
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        if printing:
            # Print Outputs
            print('\n"{}"'.format(text.description.encode('utf-8')))
            print('bounds: {}'.format(','.join(vertices)))
        # Have to encode in utf-8 to avoid some error
        labels = np.append(labels, text.description.encode('utf-8'))
        bounds.append(text.bounding_poly)

    return labels, bounds


def draw_boxes(path, bounds, color, width=5):
    image = Image.open(path)
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y], fill=color, width=width)
    return image


def detectAndAnnotate(imagePath, showing=False):
    # detect_text_openCV(imagePath)
    labels, bounds = detect_text_vision(imagePath)
    annotatedImage = draw_boxes(imagePath, bounds, 'red')
    if showing:
        cv2.imshow('Annotated Image', annotatedImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return annotatedImage, labels, bounds
