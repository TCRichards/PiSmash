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


# Assigns the ranks depicted in the screenshot of the provided results screen to the input game
def assignRanks(imagePath, game, printing=False, showing=False):
    if printing:
        print('Analyzing Results Screen')
    sortedRanks = rankGame(imagePath, draw_output=showing)  # IMPORTANT: Ranks must be pre-sorted in ascending player order
    for playerNum, rank in enumerate(sortedRanks, 1):       # Search through playerNumbers starting at 1
        for player in game.players:
            if player.playerNum == 'P{}'.format(playerNum):
                player.rank = rank
                break                  # Breaks out of the inner loop -> next rank
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
