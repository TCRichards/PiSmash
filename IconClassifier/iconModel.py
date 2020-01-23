'''
Uses training images stored in directory to build neural network
Author: Thomas Richards
Date Modified: 6/18/19
'''
import os
from inspect import getsourcefile

from . import makeIcons
import modelHelper

trainingDir = makeIcons.trainingDir
testingDir = makeIcons.testingDir


current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
modelPath = os.path.join(parent_dir, 'iconModel.h5')

# Image dimensions
num_rows, num_cols = makeIcons.num_rows, makeIcons.num_cols


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
    "piranhaPlant": 54,     # May need to include other color icons for this one
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
    "zeroSuitSamus": 77,
}


def isCharacter(label):
    if label.upper() in [k.upper() for k in charDict.keys()]:
        return label.lower()
    label = label.upper()
    if label == 'BANJO':
        return 'banjo&kazooie'
    elif label == 'CAPTAIN':
        return 'captainFalcon'
    elif label == 'PIT':
        return 'darkPit'
    elif label == 'SAMUS':
        return 'darkSamus'
    elif label == 'DIDDY':
        return 'diddyKong'
    elif label == 'DONKEY':
        return 'donkeyKong'
    elif label == 'DUCK':
        return 'duckHunt'
    elif label == 'ICE':
        return 'iceClimbers'
    elif label == 'POKEMON':
        return 'pokemonTrainer'
    elif label == 'DEDEDE':
        return 'kingDedede'
    elif label == 'ROOL':
        return 'kingKRool'
    elif label == 'MAC':
        return 'littleMac'
    elif label == 'MEGA':
        return 'megaMan'
    elif label == 'META':
        return 'metaKnight'
    elif label == 'FIGHTER':
        return 'miiFighter'
    elif label == 'GUNNER':
        return 'miiGunner'
    elif label == 'BRAWLER':
        return 'miiBrawler'
    elif label == 'SWORDFIGHTER':
        return 'miiSwordfighter'
    elif label == 'WATCH':
        return 'mrGame&Watch'
    elif label == 'PAC':
        return 'pac-man'
    elif label == 'PLANT':
        return 'piranhaPlant'
    elif label == 'TOON':
        return 'toonLink'
    elif label == 'YOUNG':
        return 'youngLink'
    elif label == 'ZERO':
        return 'zeroSuitSamus'
    elif label == 'RANDOM': # Catch the random
        return 'random'
    return None


def makeModel():
    x_train, y_train = modelHelper.getTrainingData(trainingDir, charDict, num_rows, num_cols)

    EPOCHS = 75
    BATCH_SIZE = 32

    return modelHelper.makeImageModelIcon(x_train, y_train, modelPath, len(charDict), EPOCHS, BATCH_SIZE)


def testModel():
    x_test, y_test = modelHelper.getTestingData(testingDir, charDict, num_rows, num_cols)
    print(x_test.shape, y_test.shape)
    modelHelper.testModel(x_test, y_test, modelPath, charDict)


def main():     # Main function allows us to create and test our model seperately
    # makeModel()
    testModel()


# main()
