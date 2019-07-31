from textRecognition import selectDetect as sd
from textRecognition import resultsDetect as rd
from PiCamera import readStream
from ScreenClassifier.ScreenModel import screenDict, num_rows, num_cols
from IconClassifier.iconModel import charDict
from modelHelper import makePrediction

import glob
from tensorflow import keras
import os
from PIL import Image
import threading
import numpy as np
import time

curDir = os.path.dirname(__file__)

iconModelPath = os.path.join(curDir, 'iconModelPrototype.h5')
screenModelPath = os.path.join(curDir, 'screenModelPrototype.h5')
screenDir = readStream.imageDir


class GameStatus:
    def __init__(self):
        self.status = 'Select'


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
    # if sortedNames[0] is lastFile:  # Return the most recent as long as it wasn't the last used
    #     return sortedNames[1]
    if len(sortedNames) > 1:
        return sortedNames[1]
    return sortedNames[0]


if __name__ == '__main__':
    status = GameStatus()
    screenModel = keras.models.load_model(screenModelPath)
    # Constantly monitor the stream and take screenshots using a separate thread
    streamThread = threading.Thread(target=readStream.stream, daemon=True)  # Runs forever
    # Debugging ignoring stream
    # streamThread.start()    # Give the other thread a 3 second headstart

    time.sleep(3)

    lastFile = None
    while True:
        import pdb
        pdb.set_trace()

        latestFile = getMostRecentFile(screenDir, lastFile)
        rawIm = Image.open(latestFile)
        newIm = rawIm.resize((num_rows, num_cols))                  # Rescale the image to num_rows x num_cols
        img = np.array(newIm).astype(float) / 255.          # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
        img = img.reshape((1,) + img.shape)                 # Make 4D so that model can interpret
        guess = makePrediction(screenModel, screenDict, img)

        # How to handle the current reading? Most of the time we'll discard but take note if there's a transition
        if status.status == 'Select':
            if guess == 'Game':
                print('Changing status to game')
                status.status = 'Game'
        elif status.status == 'Game':
            if guess == 'Victory':
                print('Changing status to victory')
                status.status = 'Victory'
        elif status.status == 'Victory':
            if guess == 'Select':
                print('Chaging status to select')
                status.status = 'Select'

        lastFile = latestFile
