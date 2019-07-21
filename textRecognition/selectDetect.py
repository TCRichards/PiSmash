import sys
import os

sys.path.append(sys.path[0] + '/..')    # Allows us to pull this module from the parent directory
from IconClassifier import iconModel
import googleText as goog
from player import Player   # Class wrapping a Player's character, tag, and rank

import cv2
import numpy as np

import pdb

curDir = os.getcwd()
screenDir = curDir + '/SelectScreens/'
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
    playerColumn = []
    tagColumn = []
    charColumn = []

    # Functions that we use to filter the meaning behind each detected text
    def isPlayerNum(label):    # Right now this double counts CPU
        isPNum = False
        # If the label matches P{} for any integer 1-9, then this will be True
        for i in range(1, 10):
            isPNum |= label == 'P{}'.format(i) or label == 'CPU'
        return isPNum

    def isCharacter(label):
        return iconModel.isCharacter(label)

    # Iterate over all the text and sort into proper lists
    for i, byteLabel in enumerate(bottomLabels):
        label = byteLabel.decode('unicode_escape')  # Converts the label from bytes to string
        if isCharacter(label):
            formattedName = isCharacter(label)  # Convert the label to the same format as stored in iconModel's charDict
            charColumn.append([formattedName, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y])
        elif isPlayerNum(label):
            playerColumn.append([label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y])
        else:
            tagColumn.append([label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y])

    # Goes through the contents of otherCol and keeps only tag names
    def filterTags(charCol, playerCol, otherCol):
        charHeight = charCol[0][2]
        playerNumHeight = playerCol[0][2]

        for o in otherCol:  # Tag names are the only text located between player numbers and character names
            if not charHeight + 20 < o[2] < playerNumHeight - 20:
                otherCol.remove(o)

        for o in otherCol:
            if o[0] == 'Player':   # In order to get the proper player number, look for an integer directly to the right
                possibleNums = sorted(otherCol, key=lambda entry: abs(entry[1] - o[1]))
                for entry in possibleNums:
                    val = entry[0]
                    try:
                        int(val)    # Will throw a TypeError exception if not a number
                        otherCol.remove(entry)    # After we find the number, remove it from the list
                        o[0] += ' ' + val
                        break       # Move onto the next input
                    except ValueError:
                        pass

    filterTags(charColumn, playerColumn, tagColumn)  # Filter the tagColumn so that it only contains player tags

    # Matches each player name with character name, and stores the matched duple in a Player object
    def matchLabels(charCol, playerCol, tagCol):
        pdb.set_trace()
        players = []
        for i in range(len(charCol)):
            charName = charCol[i][0]    # Name of the character
            charX = charCol[i][1]       # x-position of one of the vertices
            # Sort player names by distance to the character we're looking at
            sortedPlayers = sorted(playerCol, key=lambda play: abs(play[1] - charX))
            sortedTags = sorted(tagCol, key=lambda tag: abs(tag[1] - charX))
            playerTag = sortedTags[0][0]
            playerNum = sortedPlayers[0][0]
            newPlayer = Player(playerTag, charName, playerNum, -1)
            players.append(newPlayer)
        return players

    players = matchLabels(charColumn, playerColumn, tagColumn)  # Matches each text label to fully describe each player

    return players


loadImage(imagePath, printing=False, showing=False)
