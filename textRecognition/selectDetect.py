'''
Script that loads an image from the select screen and captures information about each player in the game
Stores information about character played, player name, player number in a Player object
Date Created: 7/21/2019
'''
import os
import sys
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)
from IconClassifier import iconModel
from . import googleText as goog
from .player import Player   # Class wrapping a Player's character, tag, and rank
from .game import Game

import cv2
import numpy as np

curDir = os.getcwd() + '/textRecognition/'
screenDir = curDir + '/SelectScreens/'
imagePath = screenDir + 'screen4.png'


def imageToGame(path, printing=False, showing=False):
    import pdb
    pdb.set_trace()
    labels, bounds = goog.detect_text_vision(path, printing=printing)
    bottomLabels = np.array([])
    bottomBounds = np.array([])
    imgHeight = cv2.imread(path).shape[0]
    for i in range(len(bounds)):
        if bounds[i].vertices[0].y >= imgHeight * 2 // 3:  # Only look at the text near the bottom of the screen
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
    for i, label in enumerate(bottomLabels):
        if isCharacter(label):
            formattedName = isCharacter(label)  # Convert the label to the same format as stored in iconModel's charDict
            charColumn.append([formattedName, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y])
        elif isPlayerNum(label):
            playerColumn.append([label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y])
        else:
            tagColumn.append([label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y])

    charHeight = charColumn[0][2]
    playerNumHeight = playerColumn[0][2]

    # Goes through the contents of otherCol and keeps only tag names
    def filterTags(tagCol):
        for o in tagCol:  # Tag names are the only text located between player numbers and character names
            if not charHeight + 20 < o[2] < playerNumHeight - 20:
                tagCol.remove(o)

        for o in tagCol:
            if o[0] == 'Player':   # In order to get the proper player number, look for an integer directly to the right
                possibleNums = sorted(tagCol, key=lambda entry: abs(entry[1] - o[1]))
                for entry in possibleNums:
                    val = entry[0]
                    try:
                        int(val)    # Will throw a TypeError exception if not a number
                        tagCol.remove(entry)    # After we find the number, remove it from the list
                        o[0] += ' ' + val
                        break       # Move onto the next input
                    except ValueError:
                        pass

    filterTags(tagColumn)  # Filter the tagColumn so that it only contains player tags

    # Matches each player name with character name, and stores the matched duple in a Player object
    def matchLabels(charCol, playerCol, tagCol):
        players = []
        for i in range(len(charCol)):
            charName = charCol[i][0]    # Name of the character
            charX = charCol[i][1]       # x-position of one of the vertices
            # Sort player names by distance to the character we're looking at
            sortedPlayers = sorted(playerCol, key=lambda play: abs(play[1] - charX))
            sortedTags = sorted(tagCol, key=lambda tag: abs(tag[1] - charX))
            playerTag = sortedTags[0][0]
            playerNum = sortedPlayers[0][0]
            if playerNum == 'CPU':
                playerTag = 'CPU'   # CPU doesn't have a tag so just copy 'CPU' over
            newPlayer = Player(playerTag, charName, playerNum, -1)
            players.append(newPlayer)
            playerCol.remove(sortedPlayers[0])
            tagCol.remove(sortedTags[0])

        return players

    players = matchLabels(charColumn, playerColumn, tagColumn)  # Matches each text label to fully describe each player
    game = Game(players)
    return game


if __name__ == '__main__':
    game = imageToGame(imagePath, printing=False, showing=False)
    for player in game.players:
        player.printOut()
