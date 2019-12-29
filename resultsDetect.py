'''
Given an image from the results screen, this script is used to determine each player's rankings
and other stats, given the list of players in the game (determined by selectDetect.py) as input
and modifies each player's 'rank' field with the proper position

Authors: Thomas Richards and Nick Konz
Date Modified: 12/26/2019
'''

import os
import numpy as np
from collections import OrderedDict


import textRecognition.googleText as goog
from textRecognition.game import Game
from textRecognition.player import Player
import objectRecognition.objDetModelHelper as objDetect

curDir = os.path.dirname(__file__)
vicScreenDir = os.path.join(curDir, 'textRecognition', 'victoryScreens')
resultsScreenDir = os.path.join(curDir,'textRecognition', 'resultsScreens')

resultsImagePath = os.path.join(resultsScreenDir, 'realResults0.png')
victoryImagePath = os.path.join(vicScreenDir, 'realVic0.png')


# labels and bounds inputs are solely from text recognition; rank detection is done separately
def rankOrder(imagePath, labels, bounds, printing=False):
    #playerBounds = []   # Make an array storing the bounding boxes for each time player number is seen
    playerNums = [] # all detected "P#" text

    # Calculates the number of players present by searching for ascending 'P#' numbers
    for i in range(1, 9):
        if ('P{}'.format(i)) in labels:
            index = np.where(labels == ('P{}'.format(i)))[0][0]
            playerNums.append(labels[index])

    # We only need the x position of the player tag to determine order
    # xBoundsPlayerNum = [bound.vertices[0].x for bound in playerBounds]

    detectedRankObjs = objDetect.detectRanks(imagePath)
    xBoundsRanks = [box.xmin for box in detectedRankObjs[0]]
    ranks = [objDetect.ranktoInt(rankLabel) for rankLabel in detectedRanks[1]] # list of ranks as ints

    # sorted from left to right onscreen
    sortedPlayerNums = OrderedDict(sorted(zip(playerNums, xBoundsPlayerNum), key=lambda t: t[1]))
    sortedRanks = OrderedDict(sorted(zip(ranks, xBoundsRanks), key=lambda t: t[1]))

    # now that P#s are matched to ranks, sort these with respect to such ranks
    scoreDict = OrderedDict(sorted(zip(sortedPlayerNums.keys(), sortedRanks.keys()), key=lambda t: t[1]))   # Sorts the player numbers with the x coordinates in ascending order
    if printing:
        print('Rankings are:')
        for item in scoreDict.items():
            print('P{}'.format(item[0]))
    return scoreDict.keys()     # Returns a list of players 'P{}' in sorted order of rank


def rankGame(imagePath, game, printing=False, showing=False):
    annotated_image, labels, bounds = goog.detectAndAnnotate(imagePath, printing=printing, showing=showing)

    sortedPlayers = rankOrder(imagePath, labels, bounds, printing=False)   # List of players 'P{}' order of rank
    for rank, playerNum in enumerate(sortedPlayers, 1):
        for player in game.players:
            if player.playerNum == playerNum:
                player.rank = rank
                break           # Breaks out of the inner loop -> next rank

    return game


if __name__ == '__main__':
    THOMATO = Player('THOMATO', 'Shulk', 'P1', None)
    BEEF = Player('BEEF', 'Ike', 'P2', None)

    sampleGame = Game([THOMATO, BEEF])
    print('Before analysis')
    sampleGame.printOut()

    rankGame(resultsImagePath, sampleGame, printing=False, showing=True)

    print('\nAfter analysis')
    sampleGame.printOut()
