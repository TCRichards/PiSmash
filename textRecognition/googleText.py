# export GOOGLE_APPLICATION_CREDENTIALS=kyourcredentials.json
import io
import cv2
from PIL import Image, ImageDraw
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Explicitly add google credentials to the command line if not there already
curDir = os.getcwd() + '/textRecognition/'
imagePath = curDir+'resultsScreens/SSBUVictoryMarth.jpg'
credentialsPath = curDir+'Pi Smash-e156332f76fc.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentialsPath

# Instantiates a client
client = vision.ImageAnnotatorClient()

def detect_text(path):
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
    print('Texts:')

    for text in texts:
        labels = np.append(labels, text.description.encode('utf-8'))   # Have to encode in utf-8 to avoid some error
        print('\n"{}"'.format(text.description.encode('utf-8')))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

        bounds.append(text.bounding_poly)

    return labels, bounds

def draw_boxes(path, bounds, color,width=5):
    image = Image.open(path)
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y],fill=color, width=width)
    return image

labels, bounds = detect_text(imagePath)

# How do we take this image bounding data and interpret it to count the number of players

# Calculates the number of players present
for numPlayers in range(8,1,-1):
    if ('P' + str(numPlayers)).encode('utf-8') in labels:   # Don't forget about utf-8 encoding from earlier
        break

for label in labels:
    print(label)

annotatedIm = draw_boxes(imagePath, bounds, 'green')
plt.imshow(annotatedIm)
plt.show()

# If all we care about is place recieved, not anything to do with stats, we can get a much easier shot of that during the victory pose
'''
# General pattern for end screen seems to be different for different numbers of players:
For 2 Players {
    Smash
    Stock/
    2/Final
    Destination
    for number of players:
        Place Received (doesn't recognize 1, but can use deduction)
        Character name
        Player Number

    All player names in a row

    for each player:
        Stat definition
        Stat result

    'A' and then 'OK'
    Junk corresponding to god knows what
}
For Time (don't implement because this is bitch mode){
    b'8-Player'
    b'Smash'
    b'Time/6'
    b'min.'
    b'/'
    b'Big'
    b'Battlefield'

    We'll need to use position data in order to organize like pieces of data
    All player names not necessarily in order
    All character names in same order as player names
    Player names in no particular order (note that two-worded names register as two strings)

}
'''
