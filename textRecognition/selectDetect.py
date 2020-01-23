'''
Script that loads an image from the select screen and captures information about each player in the game
Stores information about character played, player name, player number in a Player object
Date Created: 7/21/2019
'''
import os
import sys
from inspect import getsourcefile
import cv2
import numpy as np

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)
from IconClassifier import iconModel
import databaseManager as dbm

try:
    import googleText as goog
    from player import Player   # Class wrapping a Player's character, tag, and rank
    from game import Game
except ModuleNotFoundError or ImportError:
    from . import googleText as goog
    from .player import Player   # Class wrapping a Player's character, tag, and rank
    from .game import Game


curDir = os.path.dirname(__file__)
screenDir = os.path.join(curDir, 'charSelectScreens')
imagePath = os.path.join(screenDir, 'realChar0.png')


# TODO: Currently doesn't work first characters that are more than 1 word (e.g. Dark Pit)
def imageToGame(path, printing=False, showing=False):
    # We only need to see the raw results if we're running the script from this file
    labels, bounds = goog.detect_text_vision(path, printing=(printing and __name__ == '__main__'))
    bottomLabels = np.array([])
    bottomBounds = np.array([])
    imgHeight = cv2.imread(path).shape[0]
    for i in range(len(bounds)):
        if bounds[i].vertices[0].y >= imgHeight * 1 // 2:  # Only look at the text near the bottom of the screen
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
            isPNum = isPNum or (label == 'P{}'.format(i) or label == 'CPU')
        return isPNum

    def isCharacter(label):
        return iconModel.isCharacter(label)

    # Iterate over all the text and sort into proper lists

    avoidedCPU_idxs = set([])   # Store a set of the indices of CPU labels to avoid counting
    for i, label in enumerate(bottomLabels):
        if i in avoidedCPU_idxs:
            continue
        if isCharacter(label):
            formattedName = isCharacter(label)  # Convert the label to the same format as stored in iconModel's charDict
            charColumn.append([formattedName, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y])
        elif isPlayerNum(label):
            if label == 'CPU':  # Since CPU is counted as a player number AND a tag, we have to add it to both
                closestCPU_dist = np.inf
                closestCPU_idx = 0
                for j in range(len(bottomBounds)):  # Search through all the labels and find the closest one that's also a CPU
                    if j == i:  # Don't count the same distance
                        continue
                    if bottomLabels[j] == 'CPU':
                        distance_x = abs(bottomBounds[j].vertices[0].x - bottomBounds[i].vertices[0].x)
                        print('Distance From {} to {} = {}'.format(i, j, distance_x))
                        if j not in avoidedCPU_idxs:
                            if distance_x < closestCPU_dist:
                                closestCPU_idx = j
                                closestCPU_dist = distance_x        # Update the closest distance
                    # if bottomLabels[j] == 'CPU' and bottomLabels[j] not in avoidedCPU_idxs:
                    #     if abs(bottomBounds[j].vertices[0].x - bottomBounds[i].vertices[0].x) < closestCPU_dist:
                    #         closestCPU_idx = j
                avoidedCPU_idxs.add(closestCPU_idx)  # Mark j as an index to avoid to prevent double-counting

                # If the label we're looking at is higher on the screen, match that with the player tag

                if bottomBounds[i].vertices[0].y < bottomBounds[j].vertices[0].y:
                    tagColumn.append([label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y])
                    playerColumn.append([label, bottomBounds[j].vertices[0].x, bottomBounds[j].vertices[0].y])
                else:
                    tagColumn.append([label, bottomBounds[j].vertices[0].x, bottomBounds[j].vertices[0].y])
                    playerColumn.append([label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y])

            else:
                playerColumn.append([label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y])
        else:
            tagColumn.append([label, bottomBounds[i].vertices[0].x, bottomBounds[i].vertices[0].y])

    # Lists storing the relevant labels as well as the bottom x & y coordinates of each
    charHeight = charColumn[0][2]   # Stores the players found ['P1', x_cord, y_cord]
    playerNumHeight = playerColumn[0][2]    # Stores the characters found ['isabelle', x_cord, y_cord]

    # Filtered all possible tags to only those that have been registered in the database
    filteredTags = list(filter(lambda entry: (dbm.playerExists(entry[0])), tagColumn))
    # Matches each player name with character name, and stores the matched duple in a Player object
    def matchLabels(charCol, playerCol, tagCol):
        players = []
        for i in range(len(tagCol)):
            if not dbm.playerExists(tagCol[i][0]): continue     # Only run the matching if this player is registered
            playerTag = tagCol[i][0]
            tagX, tagY = tagCol[i][1], tagCol[i][2]             # x, y coordinates of the player tag

            sortedPlayers = sorted(playerCol, key=lambda play: abs(play[1] - tagX)) # Sort player number by x position
            sortedChars = sorted(charCol, key=lambda char: abs((char[2] - tagY))**2 + (char[1] - tagX) ** 2)     # Sort character played by absolute position
            playerNum = sortedPlayers[0][0]
            charName = sortedChars[0][0]
            if playerTag == 'CPU':
                playerNum = 'CPU'   # CPU doesn't have a tag so just copy 'CPU' over
            newPlayer = Player(playerTag, charName, playerNum, -1)
            players.append(newPlayer)

        return players

    players = matchLabels(charColumn, playerColumn, filteredTags)  # Matches each text label to fully describe each player
    game = Game(players)

    if printing:
        for player in players:
            player.printOut()
    return game


if __name__ == '__main__':
    game = imageToGame(imagePath, printing=True, showing=False)
    for player in game.players:
        player.printOut()
