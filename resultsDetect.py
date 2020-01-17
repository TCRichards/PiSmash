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
from objectRecognition.rankDetector.rankGame import rankGame

curDir = os.path.dirname(__file__)
resultsScreenDir = os.path.join(curDir,'objectRecognition', 'rankDetector', 'inputFolder')
resultsImagePath = os.path.join(resultsScreenDir, 'realResults0.png')


# labels and bounds inputs are solely from text recognition; rank detection is done separately
def rankOrder(imagePath, printing=False):
    playerBounds = []   # Make an array storing the bounding boxes for each time player number is seen
    playerNums = []     # all detected "P#" text

    # Calculates the number of players present by searching for ascending 'P#' numbers
    for i in range(1, 9):
        if ('P{}'.format(i)) in labels:
            index = np.where(labels == ('P{}'.format(i)))[0][0]
            playerNums.append(labels[index])

    xBoundsPlayerNum = [bound.vertices[0].x for bound in playerBounds]   # We only need the x position of the player tag to determine order

    detectedRankBoxes = objDetect.detectRanks(imagePath)
    xBoundsRanks = [box.xmin for box in detectedRankBoxes]
    ranks = rankGame(imagePath)     # list of ranks as ints, sorted in ascending player order

    # sorted from left to right onscreen
    # if below isn't working, check that I sorted things correctly below
    sortedPlayerNums = OrderedDict(sorted(zip(xBoundsPlayerNum, playerNums), key=lambda t: t[0]))

    # now that P#s are matched to ranks, sort these with respect to such ranks
    scoreDict = OrderedDict(sorted(zip(sortedPlayerNums.keys(), sortedRanks.keys()), key=lambda t: t[1]))   # Sorts the player numbers with the x coordinates in ascending order
    if printing:
        print('Rankings are:')
        for item in scoreDict.items():
            print('P{}'.format(item[0]))
    return scoreDict.keys()     # Returns a list of players 'P{}' in sorted order of rank


def assignRanks(imagePath, game, showing=False):
    sortedRanks = rankGame(imagePath, draw_output=showing)  # Ranks are pre-sorted in ascending player order
    for playerNum, rank in enumerate(sortedRanks, 1):   # Search through playerNumbers starting at 1
        for player in game.players:
            if player.playerNum == 'P{}'.format(playerNum):
                player.rank = rank
                break           # Breaks out of the inner loop -> next rank
    return game


if __name__ == '__main__':
    THOMATO = Player('THOMATO', 'HERO', 'P1', None)
    BEEF = Player('BEEF', 'Ike', 'P2', None)
    LONG = Player('LONG', 'Villager', 'P3', None)
    BIRD = Player('BIRD', 'Marth', 'P4', None)


    sampleGame = Game([THOMATO, BEEF, LONG, BIRD])
    print('Before analysis')
    sampleGame.printOut()

    assignRanks(resultsImagePath, sampleGame, showing=True)

    print('\nAfter analysis')
    sampleGame.printOut()
