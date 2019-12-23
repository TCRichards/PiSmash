import io
import cv2
import os
import numpy as np
from PIL import Image, ImageDraw

# Imports the Google Cloud client library
from google.cloud import vision

try:
    import imagePreProcessing as preproc
except ModuleNotFoundError:
    from . import imagePreProcessing as preproc

# Explicitly add google credentials to the command line if not there already
curDir = os.path.dirname(__file__)

imagePath = os.path.join(curDir, 'selectScreens/screen3.jpg')
credentialsPath = os.path.join(curDir, 'visionCredentials.json')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentialsPath

# Instantiates a client
client = vision.ImageAnnotatorClient()


# NOTE: The Vision API is unable to detect the numbers '1' or '2' from the results screen (due to their
# wacky font).  I tried preprocessing the images to improve the clarity of these digits to no avail
# Looks like the only place we can consistently gather position is from the victory screen once the
# rankings are shown.  Do we need to make a separate classification between victory pose and victory-ranking screen?
# We could also train our own model using ImageAI solely to search for the position of these numbers, which
# are always present on the results screen
def detect_text_vision(path, printing=False):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    # Attempts to improve text detection by preprocessing the image first

    # processedPath = path[:-4] + '_process.png'
    # preproc.smoothImage(path, processedPath, showing=True)
    # preproc.rotateImage(path, processedPath, showing=True)
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    labels = np.array([])
    bounds = []

    for text in texts:
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        if printing:
            # Print Outputs
            print('\n"{}"'.format(text.description))
            print('bounds: {}'.format(','.join(vertices)))
        # Have to encode in utf-8 to avoid some error
        labels = np.append(labels, text.description)
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


def detectAndAnnotate(imagePath, printing=False, showing=False):
    # detect_text_openCV(imagePath)
    labels, bounds = detect_text_vision(imagePath, printing=printing)
    annotatedImage = np.array(draw_boxes(imagePath, bounds, 'red'))     # Needs to be an array for cv2 to show
    if showing:
        cv2.imshow('Annotated Image', cv2.cvtColor(annotatedImage, cv2.COLOR_BGR2RGB))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return annotatedImage, labels, bounds


if __name__ == '___main__':
    detect_text_vision(os.path.join(curDir, 'textExamples/example_01.jpg'))
