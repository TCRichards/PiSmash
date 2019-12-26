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

import sqlite3
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


# Simple struct that stores the current state of the game from ['character select', 'Black'...]
class GameStatus:
    def __init__(self):
        self.status = None


# TODO: Creates a sample game to test text recognition
def makeGame():
    game = sd.loadImage(sd.imagePath)       # Create the game object using selectDetect's OCR
    rd.loadImage(rd.imagePath, game)        # Fill in the ranking at the end of the game using resultsDetect's OCRw


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
    streamThread = threading.Thread(target=readStream.captureMedia, args=('exampleVideos/smashVid2_short.mp4', 0.1), daemon=True)  # Runs forever
    # Debugging ignoring stream
    streamThread.start()

    time.sleep(3)   # Give the other thread a 3 second headstart (needs to fully launc before we can proceed)

    game = makeSampleGame()
    lastFile = ''

    queueSize = 3
    classifyQueue = deque(maxlen=queueSize)         # Stores the 'maxlen' most recent classifications for comparison

    while True:
        try:
            latestFile = getMostRecentFile(screenDir, lastFile) # Retrieve the most recent screenshot
            if latestFile is None:                              # If there's no new screenshot, continue
                continue

            rawIm = Image.open(latestFile)
            newIm = rawIm.resize((num_rows, num_cols))          # Rescale the image to num_rows x num_cols
            img = np.array(newIm).astype(float) / 255.          # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
            img = img.reshape((1,) + img.shape)                 # Make 4D so that model can interpret
            guess = makePrediction(screenModel, screenDict, img)# String prediction of the screen type

            # Keep the queue size limited to queueSize and add the new element
            if len(classifyQueue) >= queueSize:
                classifyQueue.pop()
            classifyQueue.appendleft(guess)

            # Check if all of the elements match.  If they do, we're confident about the result and proceed
            if classifyQueue.count(classifyQueue[0]) >= queueSize:
                guess = classifyQueue[0]
            else:
                raise ValueError  # We will manually catch this error below
            print(guess)
            # FSM chooses when to apply text recognition based on guess and current state
            if guess == "Stage-Select" or guess == "Character-Select":
                guess == "Select"

            if status.status is None:
                if guess == 'Select':
                    status.status = 'Select'
                    game = sd.imageToGame(latestFile, printing=True)  # Apply recognition the first time select is

            # TODO: What about when people change character within a select screen? This only applies
            # TR once. Leave as is for now
            elif status.status == 'Select':
                if guess == 'Game':
                    status.status = 'Game'

            # TODO: How it's currently implemented this will cause issues with the starts of victory screens
            # when the results aren't clear
            elif status.status == 'Game':
                if guess == 'Victory':
                    status.status = 'Victory'
                    rd.rankGame(latestFile, game, printing=True)    # Take the results of the game and update player ranks
                    for player in game.players:     # Print out the game's results
                        player.printOut()
                    status.status = None

        except ValueError:
            pass

        finally:    # We always need to update the files regardless of if the classification was correct
            lastFile = latestFile   # Keep around the last file's name so it can be used to avoid double-counting
            if latestFile is not None:
                os.remove(latestFile)   # Remove the example file from the directory to avoid clutter and false positives
