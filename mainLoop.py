from textRecognition import selectDetect as sd
from textRecognition import resultsDetect as rd
from PiCamera import readStream
from ScreenClassifier.ScreenModel import screenDict, num_rows, num_cols
from IconClassifier.iconModel import charDict

from tensorflow import keras
import os
from PIL import Image
import threading
import numpy as np
import pdb


iconModelPath = 'iconModelPrototype.h5'
screenModelPath = 'screenModelPrototype.h5'
screenDir = 'PiCamera/screenShots/'


def makeGame():
    game = sd.loadImage(sd.imagePath)
    rd.loadImage(rd.imagePath, game)


def loadModels():
    iconModel = keras.models.load_model(iconModelPath)
    screenModel = keras.models.load_model(screenModelPath)
    return iconModel, screenModel


def getMostRecentFile(directory):
    """Iterates through all files that are under the given path."""
    for cur_path, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(cur_path, filename)


def main():
    iconModel, screenModel = loadModels()
    # Constantly monitor the stream and take screenshots using a separate thread
    # streamThread = threading.Thread(target=readStream.stream, daemon=True)  # Runs forever
    while True:
        latestFile = max(getMostRecentFile(screenDir), key=os.path.getmtime)
        rawIm = Image.open(latestFile)
        newIm = rawIm.resize((num_rows, num_cols))                  # Rescale the image to num_rows x num_cols
        img = np.array(newIm).astype(float) / 255.          # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
        img = img.reshape((1,) + img.shape)                 # Make 4D so that model can interpret
        outputs = screenModel.predict(img)
        matchIdx = np.argmax(outputs)
        screenType = list(screenDict.keys())[matchIdx]
        print(screenType)


main()
