import sys
sys.path.append('IconClassifier/')
import iconModel
import googleText as goog
from player import Player   # Class wrapping a Player's character, tag, and rank

import cv2
import numpy as np
import sys


screenDir = 'textRecognition/SelectScreens/'
imagePath = screenDir + 'screen6.jpg'


def loadImage(path, printing=False, showing=False):
    labels, bounds = goog.detect_text_vision(path, printing=printing)
    bottomLabels = np.array([])
    bottomBounds = np.array([])
    for i in range(len(bounds)):
        if bounds[i].vertices[0].y >= 500:  # Only look at the text near the bottom of the screen
            bottomLabels = np.append(bottomLabels, labels[i])
            bottomBounds = np.append(bottomBounds, bounds[i])

    annotated_image = goog.draw_boxes(path, bottomBounds, 'red')
    if showing:
        # Display the image
        cv2.imshow('Image', np.array(annotated_image))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # These lists will store relevant text and positions
    playerColumns = []
    otherColumns = []
    charColumns = []

    # Functions that we use to filter the meaning behind each detected text
    def isPlayer(label):    # Right now this double counts CPU
        return 'P' in label or 'CPU' in label

    def isCharacter(label):
        charDict = iconModel.charDict
        charNames = charDict.keys()
        capChars = [name.upper() for name in charNames]
        return label.upper() in capChars or label == 'Random'

    def isOther(label):
        return not isOther() and not isCharacter

    # Iterate over all the text and sort into proper lists
    for i, byteLabel in enumerate(bottomLabels):
        label = byteLabel.decode('unicode_escape')
        if isCharacter(label):        # Doesn't deal properly with CPU, since it appears twice
            charColumns.append((label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y))
        elif isPlayer(label):  # Checking for charNames will need to make 100% names match, which they don't
            playerColumns.append((label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y))
        else:
            otherColumns.append((label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y))

    # Matches each player name with character name, and stores the matched duple in a Player object
    def matchTagsToChars(charCols, playerCols):
        players = []
        for i in range(len(charCols)):
            charName = charCols[i][0]    # Name of the character
            charX = charCols[i][1]       # x-position of one of the vertices
            # Sort player names by distance to the character we're looking at
            sortedPlayers = sorted(playerCols, key=lambda play: play[1] - charX)
            playerTag = sortedPlayers[0][0]
            newPlayer = Player(playerTag, charName, 0)
            players.append(newPlayer)
        return players

    players = matchTagsToChars(charColumns, playerColumns)

    if printing:
        for play in players:
            play.printOut()
        print('Other stuff... = {}'.format(otherColumns))

    return players


loadImage(imagePath, printing=True)
