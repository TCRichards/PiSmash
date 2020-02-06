'''
The main loop of the entire process (once the model(s) are trained),
including screen classification, text and object recognition, etc.
Authors: Thomas Richards and Nick Konz
'''
# Import pretty much every file & library =================
from textRecognition import selectDetect as sd
import resultsDetect as rd
from textRecognition.game import makeSampleGame
from PiCamera import readStream
from ScreenClassifier.ScreenModel import screenDict, num_rows, num_cols
from ScreenClassifier.ScreenModel import modelPath as screenModelPath
from modelHelper import makePrediction
from collections import deque
import databaseManager as dbm

import cv2
import sqlite3
import matplotlib.pyplot as plt
from tensorflow import keras
import os
import pandas as pd
from PIL import Image
import threading
import numpy as np
import time
# ========================================================


curDir = os.path.dirname(__file__)
statsPath = os.path.join(curDir, '')

iconModelPath = os.path.join(curDir, 'iconModelPrototype.h5')
screenDir = readStream.imageDir

try:
    os.mkdir(screenDir)
except FileExistsError:
    pass


# Simple struct that stores the current state of the game from ['character select', 'Black'...]
class GameStatus:

    def __init__(self):
        self.status = None
        self.statusSet = set([])

        self.analyzedCharSelect = False
        self.analyzedResults = False

    def clearGame(self):
        self.statusSet.clear()
        self.status = None


# Returns the most recent file added to a directory excluding the last file checked
def getMostRecentFile(directory, lastFile):
    fileNames = [os.path.join(screenDir, file) for file in os.listdir(screenDir)]
    if not fileNames:
        return None
    # os.path.gentime resets every time a file is examined by the program, so exclude if it's the same
    # or else we never move
    sortedNames = sorted(fileNames, key=lambda x: os.path.getctime(x))

    # If there are multiple options, the second one is the one we want (first is always a repeat)
    mostRecent = sortedNames[0]
    if mostRecent == lastFile:
        if len(sortedNames) > 1:
            return sortedNames[1]
    return sortedNames[0]   # If only one option, then take it


if __name__ == '__main__':
    status = GameStatus()
    screenModel = keras.models.load_model(screenModelPath)
    # Constantly monitor the stream and take screenshots using a separate thread
    streamThread = threading.Thread(target=readStream.captureMedia, args=('exampleVideos/smashVid2_short.mp4', 0.001), daemon=True)  # Runs forever
    # streamThread = threading.Thread(target=readStream.captureStream, daemon=True)
    # Debugging ignoring stream
    streamThread.start()

    time.sleep(4)   # Give the other thread a headstart (needs to fully launc before we can proceed)
    lastFile = ''

    classifyQueueSize = 5
    imageQueueSize = classifyQueueSize + 2
    classifyQueue = deque(maxlen=classifyQueueSize)         # Stores the 'maxlen' most recent classifications for comparison
    imageQueue = deque(maxlen=imageQueueSize)           # Store the 'maxlen' most recent images (numpy matrices)

    # Define these outside of the loop so they always exist
    game = None         # Game object to be accessed and modified by subsequent code

    while True:
        try:
            latestFile = getMostRecentFile(screenDir, lastFile) # Retrieve the most recent screenshot
            if latestFile is None:                              # If there's no new screenshot, continue
                continue

            try:
                rawIm = Image.open(latestFile)
            except OSError:
                continue
            newIm = rawIm.resize((num_rows, num_cols))          # Rescale the image to num_rows x num_cols
            img = np.array(newIm).astype(float) / 255.          # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
            img = img.reshape((1,) + img.shape)                 # Make 4D (add 1 bogus dimension) so that model can interpret
            currentGuess = makePrediction(screenModel, screenDict, img)# String prediction of the screen type

            # Keep the queue size limited to queueSize and add the new element
            if len(classifyQueue) >= classifyQueueSize:
                classifyQueue.pop()
            classifyQueue.appendleft(currentGuess)

            if len(imageQueue) >= imageQueueSize:
                imageQueue.pop()
            imageQueue.appendleft(rawIm)  # Convert the image back to 3 dimensions so we can use later

            # Check if all of the elements match.  If they do, we're confident about the result and proceed
            if classifyQueue.count(classifyQueue[0]) >= classifyQueueSize:
                guess = classifyQueue[0]    # confident guess
                # print(guess)    # Print the guess when debugging
            else:
                raise ValueError  # We will manually catch this error below

            if status.status is None or status.status == 'Other':
                if guess == 'Character-Select':
                    status.status = 'Character-Select'
                    print('\nIDENTIFIED CHARACTER SELECT SCREEN\n')

            # TODO: What about when people change character within a select screen? This only applies
            # TR once. Leave as is for now
            elif status.status == 'Character-Select':
                if guess == 'Black' and not status.analyzedCharSelect:
                    charSelectPath = os.path.join(screenDir, 'Character-Select-Read.png')
                    imageQueue.pop().save(charSelectPath)
                    game = sd.imageToGame(charSelectPath, printing=False, showing=False)  # Apply recognition the first time select
                    print('ANALYZING CHARACTER SELECT SCREENSHOT {}'.format(latestFile))
                    status.analyzedCharSelect = True

                elif guess == 'Pre-Game':
                    status.status = 'Pre-Game'
                    print('\nIDENTIFIED PRE-GAME SCREEN\n')

            elif status.status == 'Pre-Game':
                if guess == 'Game':
                    status.status = 'Game'
                    print('\nIDENTIFIED GAME SCREEN\n')

            elif status.status == 'Game':
                if guess == 'Victory':
                    status.status = 'Victory'
                    print('\nIDENTIFIED VICTORY SCREEN\n')

            elif status.status == 'Victory':
                if guess == 'Results':
                    print('\nIDENTIFIED RESULTS SCREEN\n')
                    rd.assignRanks(latestFile, game, showing=True)    # Take the results of the game and update player ranks
                    game.printOut()
                    dbm.logResults(game)
                    status.clearGame()  # Reset the game for the next use

        except ValueError:  # This is raised if not all guesses in the queue are equal
            pass

        finally:    # We always need to update the files regardless of if the classification was correct
            lastFile = latestFile   # Keep around the last file's name so it can be used to avoid double-counting
            if latestFile is not None:    # Delete the image last removed from the queue
                try:    # Remove the image if it still exists (may already have been deleted)
                    os.remove(latestFile)     # Remove the example file from the directory to avoid clutter and false positives
                except FileNotFoundError:   #  Do nothing if the file is already removed
                    pass
