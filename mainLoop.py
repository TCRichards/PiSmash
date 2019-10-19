'''
The main loop of the entire process (once the model(s) are trained), 
including screen classification, text and object recognition, etc.
Authors: Thomas Richards and Nick Konz
'''
from textRecognition import selectDetect as sd
from textRecognition import resultsDetect as rd
from PiCamera import readStream
from ScreenClassifier.ScreenModel import screenDict, num_rows, num_cols
from ScreenClassifier.ScreenModel import modelPath as screenModelPath
from modelHelper import makePrediction

from tensorflow import keras
import os
from PIL import Image
import threading
import numpy as np
import time

curDir = os.path.dirname(__file__)

iconModelPath = os.path.join(curDir, 'iconModelPrototype.h5')
screenDir = readStream.imageDir


class GameStatus:
    def __init__(self):
        self.status = None


def makeGame():
    game = sd.loadImage(sd.imagePath)
    rd.loadImage(rd.imagePath, game)


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
    streamThread = threading.Thread(target=readStream.captureMedia, args=('exampleVideos/smashVid1.MOV', ), daemon=True)  # Runs forever
    # Debugging ignoring stream
    streamThread.start()    # Give the other thread a 3 second headstart

    time.sleep(3)

    game = None
    lastFile = ''

    while True:
        # import pdb
        # pdb.set_trace()
        latestFile = getMostRecentFile(screenDir, lastFile)
        if latestFile is None:
            continue
        rawIm = Image.open(latestFile)
        newIm = rawIm.resize((num_rows, num_cols))          # Rescale the image to num_rows x num_cols
        img = np.array(newIm).astype(float) / 255.          # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
        img = img.reshape((1,) + img.shape)                 # Make 4D so that model can interpret
        guess = makePrediction(screenModel, screenDict, img)
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

        lastFile = latestFile   # Keep around the last file's name so it can be used to avoid double-counting
        os.remove(latestFile)   # Remove the example file from the directory to avoid clutter and false positives
