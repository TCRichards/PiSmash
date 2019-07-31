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


def getMostRecentFile(directory):
    fileNames = [os.path.join(screenDir, file) for file in os.listdir(screenDir)]
    if not fileNames:
        return None
    return max(fileNames, key=os.path.getctime)


if __name__ == '__main__':
    status = GameStatus()
    screenModel = keras.models.load_model(screenModelPath)
    # Constantly monitor the stream and take screenshots using a separate thread
    streamThread = threading.Thread(target=readStream.stream, daemon=True)  # Runs forever
    streamThread.start()    # Give the other thread a 3 second headstart

    time.sleep(3)
    while True:
        latestFile = getMostRecentFile(screenDir)
        if not latestFile:
            continue
        print(latestFile)
        rawIm = Image.open(latestFile)
        newIm = rawIm.resize((num_rows, num_cols))                  # Rescale the image to num_rows x num_cols
        img = np.array(newIm).astype(float) / 255.          # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
        img = img.reshape((1,) + img.shape)                 # Make 4D so that model can interpret
        guess = makePrediction(screenModel, screenDict, img)
        print(guess)

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
