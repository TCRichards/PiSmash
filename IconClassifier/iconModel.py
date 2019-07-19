'''
Uses training images stored in directory to build neural network
Author: Thomas Richards
Date Modified: 6/18/19
'''

import makeIcons
import sys
sys.path.append(sys.path[0] + '/..')    # Allows us to pull this module from the parent directory
import modelHelper

trainingDir = makeIcons.trainingDir
testingDir = makeIcons.testingDir


# Image dimensions
num_rows, num_cols = makeIcons.num_rows, makeIcons.num_cols

modelName = 'iconModelPrototype.h5'

# Maps character names to corresponding labels for classification
charDict = {
    "banjo&kazooie": 0,
    "bayonetta": 1,
    "bowser": 2,
    "captainFalcon": 3,
    "chrom": 4,
    "cloud": 5,
    "corin": 6,
    "daisy": 7,
    "darkPit": 8,
    "darkSamus": 9,
    "diddyKong": 10,
    "donkeyKong": 11,
    "drMario": 12,
    "duckHunt": 13,
    "falco": 14,
    "fox": 15,
    "ganondorf": 16,
    "greninja": 17,
    "hero": 18,
    "iceClimbers": 19,
    "ike": 20,
    "incineroar": 21,
    "inkling": 22,
    "isabelle": 23,
    "pokemonTrainer": 24,
    "jigglypuff": 25,
    "joker": 26,
    "ken": 27,
    "kingDedede": 28,
    "kingKRool": 29,
    "kirby": 30,
    "link": 31,
    "littleMac": 32,
    "lucario": 33,
    "lucas": 34,
    "lucina": 35,
    "luigi": 36,
    "mario": 37,
    "marth": 38,
    "megaMan": 39,
    "metaKnight": 40,
    "mewtwo": 41,
    "miiBrawler": 42,
    "miiFighter": 43,
    "miiGunner": 44,
    "miiSwordfighter": 45,
    "mrGame&Watch": 46,
    "ness": 47,
    "olimar": 48,
    "pac-man": 49,
    "palutena": 50,
    "peach": 51,
    "pichu": 52,
    "pikachu": 53,
    "piranhaPlant": 54,                 # May need to include other color icons for this one
    "pit": 55,
    "richter": 56,
    "ridley": 57,
    "ROB": 58,
    "robin": 59,
    "rosalina": 60,
    "roy": 61,
    "ryu": 62,
    "samus": 63,
    "sheik": 64,
    "shulk": 65,
    "simon": 66,
    "snake": 67,
    "sonic": 68,
    "toonLink": 69,
    "villager": 70,
    "wario": 71,
    "wiiFitTrainer": 72,
    "wolf": 73,
    "yoshi": 74,
    "youngLink": 75,
    "zelda": 76,
    "zeroSuitSamus": 77
}


def makeModel():
    x_train, y_train = modelHelper.getTrainingData(trainingDir, charDict, num_rows, num_cols)
    EPOCHS = 75
    BATCH_SIZE = 32
    return modelHelper.makeImageModel(x_train, y_train, modelName, len(charDict), EPOCHS, BATCH_SIZE)


def testModel():
    x_test, y_test = modelHelper.getTestingData(testingDir, charDict, num_rows, num_cols)
    print(x_test.shape, y_test.shape)
    modelHelper.testModel(x_test, y_test, modelName, charDict)


# Main function allows us to create and test our model seperately
def main():
    # makeModel()
    testModel()


# keep commented so we can import for the dictionary
# main()
