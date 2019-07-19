import iconModel

import cv2
import os
import numpy as np
import sys

import googleText as goog
import player
sys.path.append('IconClassifier/')

screenDir = 'textRecognition/SelectScreens/'
imagePath = screenDir+'screen4.jpg'


def loadImage(path, printing=False, showing=False):
    #imagePaths = os.listdir(screenDir)
    img = cv2.imread(path)

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
    nameColumns = []
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
            sortedPlayers = sorted(playerCols,key=lambda play: play[1] - charX)
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

def rankOrder(labels, bounds):
    playerBounds = []   # Make an array storing the bounding boxes for each time player number is seen
    # Calculates the number of players present
    for numPlayers in range(1, 9):
        if ('P' + str(numPlayers)).encode('utf-8') in labels:   # Don't forget about utf-8 encoding from earlier
            index = np.where(labels == ('P' + str(numPlayers)).encode('utf-8'))[0][0]
            playerBounds.append(bounds[index])
        else: break # If the player number isn't seen, then one less is the total number of players

    xBounds = [bound.vertices[0].x for bound in playerBounds]
    playerNums = np.arange(1, numPlayers)

    scoreDict = OrderedDict(sorted(zip(playerNums, xBounds), key = lambda t: t[1])) # Sorts the player numbers with the x coordinates in ascending order

    print('Rankings are:')
    for item in scoreDict.items():
        print('P{}'.format(item[0]))
    return

def rankOrder(labels, bounds):
    playerBounds = []   # Make an array storing the bounding boxes for each time player number is seen

    # Calculates the number of players present
    for numPlayers in range(1, 9):
        if ('P' + str(numPlayers)).encode('utf-8') in labels:   # Don't forget about utf-8 encoding from earlier
            index = np.where(labels == ('P' + str(numPlayers)).encode('utf-8'))[0][0]
            playerBounds.append(bounds[index])
        else: break # If the player number isn't seen, then one less is the total number of players

    xBounds = [bound.vertices[0].x for bound in playerBounds]
    playerNums = np.arange(1, numPlayers)

    scoreDict = OrderedDict(sorted(zip(playerNums, xBounds), key = lambda t: t[1])) # Sorts the player numbers with the x coordinates in ascending order

    print('Rankings are:')
    for item in scoreDict.items():
        print('P{}'.format(item[0]))
    return

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

loadImage(imagePath, printing=True)
