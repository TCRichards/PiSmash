'''
Uses screenshots from gameplay to make a model that classifies a game in one of three categories
Author: Thomas Richards
Date Modified: 7/27/19
'''
import sys
import os
from inspect import getsourcefile


current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

if __name__ == '__main__':  # If we're running the file here, then imports are relative to here
    import makeScreens
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

modelPath = os.path.join(parent_dir, 'screenModel.h5')

# Translates screen type to an integer
screenDict = OrderedDict({
    "Black": 0,
    "Stage-Select": 1,
    "Character-Select": 2,
    "Pre-Game": 3,
    "Game": 4,
    "Victory": 5,
    "Results": 6,
    "Other": 7
})


def makeModel():
    x_train, y_train = modelHelper.getTrainingData(trainingDir, screenDict, num_rows, num_cols)

    EPOCHS = 15
    BATCH_SIZE = 64
    return modelHelper.makeImageModel(x_train, y_train, modelPath, len(screenDict), EPOCHS, BATCH_SIZE)


def testModel():
    x_test, y_test = modelHelper.getTestingData(testingDir, screenDict, num_rows, num_cols)
    modelHelper.testModel(x_test, y_test, modelPath, screenDict)


# Main function allows us to create and test our model seperately
if __name__ == '__main__':
    makeModel()
    # testModel()
