import PIL
import keras
import cv2
import os
from PIL import Image, ImageDraw
import numpy as np
import sys

sys.path.append('IconClassifier/')
import iconModel
import googleText as goog

screenDir = 'textRecognition/SelectScreens/'

def loadImage():
    #imagePaths = os.listdir(screenDir)
    imgPath = screenDir+'screen3.jpg'
    img = cv2.imread(imgPath)

    labels, bounds = goog.detect_text_vision(screenDir+'screen3.jpg', printing=False)
    bottomLabels = np.array([]); bottomBounds = np.array([])
    for i in range(len(bounds)):
        if bounds[i].vertices[0].y >= 500:  # Only look at the text near the bottom of the screen
            bottomLabels = np.append(bottomLabels, labels[i])
            bottomBounds = np.append(bottomBounds, bounds[i])

    annotated_image = goog.draw_boxes(imgPath, bottomBounds, 'red')
    # Display the image
    cv2.imshow('Image', np.array(annotated_image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    playerColumns = []
    otherColumns = []
    nameColumns = []
    charColumns = []

    def isPlayer(label):
        return 'P' in label or 'CPU' in label
    def isCharacter(label):
        charDict = iconModel.charDict
        charNames = charDict.keys()
        capChars = [name.upper() for name in charNames]
        return label.upper() in capChars or label == 'Random'
    def isOther(label):
        return not isOther() and not isCharacter

    for i, byteLabel in enumerate(bottomLabels):
        label = byteLabel.decode('unicode_escape')
        if isCharacter(label):        # Doesn't deal properly with CPU, since it appears twice
            charColumns.append((label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y))
        elif isPlayer(label):  # Checking for charNames will need to make 100% names match, which they don't
            playerColumns.append((label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y))
        else:
            otherColumns.append((label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y))

    print('Current Players = {}'.format(playerColumns))
    print('Player Names = {}'.format(nameColumns))
    print('Other stuff.. = {}'.format(otherColumns))
    print('Current Characters = {}'.format(charColumns))

loadImage()
