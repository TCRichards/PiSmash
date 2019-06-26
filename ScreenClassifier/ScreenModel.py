'''
Uses screenshots from gameplay to make a model that classifies a game in one of three categories
Author: Thomas Richards
Date Modified: 6/24/19
'''
import makeScreens
import sys
sys.path.append(sys.path[0] + '/..')    # Allows us to pull this module from the parent directory
import modelHelper
from collections import OrderedDict

trainingDir = makeScreens.trainingDir
testingDir = makeScreens.testingDir

# Image dimensions
num_rows, num_cols = makeScreens.num_rows, makeScreens.num_cols

modelName = 'screenModelPrototype.h5'

# Translates screen type to an integer
screenDict = OrderedDict({
    "Select" : 0,
    "Game" : 1,
    "Victory" : 2
    })

def makeModel():
    x_train, y_train = modelHelper.getTrainingData(trainingDir, screenDict, num_rows, num_cols)

    EPOCHS = 4
    BATCH_SIZE = 32
    return modelHelper.makeImageModel(x_train, y_train, modelName, len(screenDict), EPOCHS, BATCH_SIZE)

def testModel():
    x_test, y_test = modelHelper.getTestingData(testingDir, screenDict, num_rows, num_cols)
    modelHelper.testModel(x_test, y_test, modelName, screenDict)


def main(): # Main function allows us to create and test our model seperately
    makeModel()
    #testModel()

main()
#=============================================
