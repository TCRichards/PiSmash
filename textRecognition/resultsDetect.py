'''
Script that loads an image from the results screen and every player's ranking
Given the list of players in the game (determined by selectDetect.py) as input,
and modifies each player's 'rank' field with the proper position
'''
import sys
import os

sys.path.append(sys.path[0] + '/..')    # Allows us to pull this module from the parent directory
from . import googleText as goog

import cv2
import numpy as np
from collections import OrderedDict

import pdb

curDir = os.getcwd() + '/textRecognition/'
screenDir = curDir + 'resultsScreens/'
imagePath = screenDir + 'vicScreen_0_2.png'


def rankOrder(labels, bounds, printing=False):
    playerBounds = []   # Make an array storing the bounding boxes for each time player number is seen
    playerNums = []
    # Calculates the number of players present
    for i in range(1, 9):
        if ('P{}'.format(i)) in labels:
            index = np.where(labels == ('P{}'.format(i)))[0][0]
            playerBounds.append(bounds[index])
            playerNums.append(labels[index])

    xBounds = [bound.vertices[0].x for bound in playerBounds]

    scoreDict = OrderedDict(sorted(zip(playerNums, xBounds), key=lambda t: t[1]))   # Sorts the player numbers with the x coordinates in ascending order
    if printing:
        print('Rankings are:')
        for item in scoreDict.items():
            print('P{}'.format(item[0]))
    return scoreDict.keys()     # Returns a list of players 'P{}' in sorted order of rank


def loadImage(path, game, printing=False, showing=False):
    labels, bounds = goog.detect_text_vision(path, printing=printing)
    annotated_image = goog.draw_boxes(path, bounds, 'red')
    if showing:
        # Display the image
        cv2.imshow('Image', np.array(annotated_image))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    sortedPlayers = rankOrder(labels, bounds, printing=False)   # List of players 'P{}' order of rank
    for rank, playerNum in enumerate(sortedPlayers, 1):
        for player in game.players:
            if player.playerNum == playerNum:
                player.rank = rank
                break           # Breaks out of the inner loop -> next rank

    return game


# loadImage(imagePath, printing=False, showing=True)
