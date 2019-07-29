from textRecognition import selectDetect as sd
from textRecognition import resultsDetect as rd
from PiCamera import readStream
from ScreenClassifier.ScreenModel import screenDict, num_rows, num_cols
from IconClassifier.iconModel import charDict
from modelHelper import makePrediction

from tensorflow import keras
import os
from PIL import Image
import threading
import numpy as np


iconModelPath = 'iconModelPrototype.h5'
screenModelPath = 'screenModelPrototype.h5'
screenDir = 'PiCamera/screenShots/'


class GameStatus:
    def __init__(self):
        self.status = 'Select'


def makeGame():
    game = sd.loadImage(sd.imagePath)
    rd.loadImage(rd.imagePath, game)


def getMostRecentFile(directory):
    def joinPaths(directory):
        # Iterates through all files that are under the given path
        for cur_path, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                yield os.path.join(cur_path, filename)
    return max(joinPaths(screenDir), key=os.path.getmtime)


if __name__ == '__main__':
    status = GameStatus()
    screenModel = keras.models.load_model(screenModelPath)
    # Constantly monitor the stream and take screenshots using a separate thread
    streamThread = threading.Thread(target=readStream.stream, daemon=True)  # Runs forever
    streamThread.start()

    while True:
        latestFile = getMostRecentFile(screenDir)
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
