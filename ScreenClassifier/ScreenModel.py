'''
Uses screenshots from gameplay to make a model that classifies a game in one of three categories
Author: Thomas Richards
Date Modified: 7/27/19
'''
import sys
import os
from inspect import getsourcefile

if __name__ == '__main__':  # If we're running the file here, then imports are relative to here
    import makeScreens
    current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
    current_dir = os.path.dirname(current_path)
    parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

    sys.path.insert(0, parent_dir)  # Add it
    import modelHelper              # Import module from parent directory
else:   # If we're running the program from mainLoop, then paths are relative to project folder
    from . import makeScreens
    import modelHelper
from collections import OrderedDict

trainingDir = makeScreens.trainingDir
testingDir = makeScreens.testingDir

# Image dimensions
num_rows, num_cols = makeScreens.num_rows, makeScreens.num_cols

modelName = 'screenModelPrototype.h5'

# Translates screen type to an integer
screenDict = OrderedDict({
    "Black": 0,
    "Character-Select": 1,
    "Game": 2,
    "Other": 3,
    "Pre-Game": 4,
    "Results": 5,
    "Stage-Select": 6,
    "Victory": 7
})


def makeModel():
    x_train, y_train = modelHelper.getTrainingData(trainingDir, screenDict, num_rows, num_cols)

    EPOCHS = 10
    BATCH_SIZE = 64
    return modelHelper.makeImageModel(x_train, y_train, modelName, len(screenDict), EPOCHS, BATCH_SIZE)


def testModel():
    x_test, y_test = modelHelper.getTestingData(testingDir, screenDict, num_rows, num_cols)
    modelHelper.testModel(x_test, y_test, modelName, screenDict)


# Main function allows us to create and test our model seperately
if __name__ == '__main__':
    makeModel()
    #testModel()
