'''
Script that loads an image from the victory screen and determines each player's ranking
Given the list of players in the game (determined by selectDetect.py) as input
and modifies each player's 'rank' field with the proper position

Author: Thomas Richards
Date Modified: 10/23/2019
'''

import os
import numpy as np
from collections import OrderedDict

try:
    import googleText as goog
    from game import Game
    from player import Player
except ModuleNotFoundError:
    from . import googleText as goog
    from .game import Game
    from .player import Player

curDir = os.path.dirname(__file__)
vicScreenDir = os.path.join(curDir, 'victoryScreens')
resultsScreenDir = os.path.join(curDir, 'resultsScreens')

resultsImagePath = os.path.join(resultsScreenDir, 'realResults0.png')
victoryImagePath = os.path.join(vicScreenDir, 'realVic0.png')


def rankOrder(labels, bounds, printing=False):
    playerBounds = []   # Make an array storing the bounding boxes for each time player number is seen
    playerNums = []

    # Calculates the number of players present by searching for ascending 'P#' numbers
    for i in range(1, 9):
        if ('P{}'.format(i)) in labels:
            index = np.where(labels == ('P{}'.format(i)))[0][0]
            playerBounds.append(bounds[index])
            playerNums.append(labels[index])

    xBounds = [bound.vertices[0].x for bound in playerBounds]   # We only need the x position of the player tag to determine order

    scoreDict = OrderedDict(sorted(zip(playerNums, xBounds), key=lambda t: t[1]))   # Sorts the player numbers with the x coordinates in ascending order
    if printing:
        print('Rankings are:')
        for item in scoreDict.items():
            print('P{}'.format(item[0]))
    return scoreDict.keys()     # Returns a list of players 'P{}' in sorted order of rank


def rankGame(path, game, printing=False, showing=False):
    annotated_image, labels, bounds = goog.detectAndAnnotate(path, printing=printing, showing=showing)

    sortedPlayers = rankOrder(labels, bounds, printing=False)   # List of players 'P{}' order of rank
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

    rankGame(resultsImagePath, sampleGame, printing=True, showing=True)

    print('\nAfter analysis')
    sampleGame.printOut()
