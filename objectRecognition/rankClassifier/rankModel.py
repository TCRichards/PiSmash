'''
Uses screenshots of victory screen player ranking numbers to create a model to recognize
these numbers and rank players accordingly for a given match
Author: Nick Konz
Date Modified: 12/20/19
'''

import sys
import os
from inspect import getsourcefile
import matplotlib.pyplot as plt


current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

if __name__ == '__main__':  # If we're running the file here, then imports are relative to here
    sys.path.insert(0, parent_dir)  # Add it
    import objDetModelHelper              # Import module from parent directory
else:   # If we're running the program from mainLoop, then paths are relative to project folder
    import objDetModelHelper
from collections import OrderedDict

# trainingDir = os.path.join(curDir, 'trainingImages/')
# validationDir = os.path.join(curDir, 'validationImages/')
# testingDir = os.path.join(curDir, 'testingImages/')

# Image dimensions
# num_rows, num_cols = makeScreens.num_rows, makeScreens.num_cols

# modelPath = os.path.join(parent_dir, 'rankModel.h5')

# Translates screen type to an integer
# screenDict = OrderedDict({
#     "Black": 0,
#     "Stage-Select": 1,
#     "Character-Select": 2,
#     "Pre-Game": 3,
#     "Game": 4,
#     "Victory": 5,
#     "Results": 6,
#     "Other": 7
# })


def makeModel():
    # x_validation, y_validation = objDetModelHelper.getValidationData(validationDir, screenDict, num_rows, num_cols)
    # x_train, y_train = objDetModelHelper.getTrainingData(trainingDir, screenDict, num_rows, num_cols)

    # EPOCHS = 100
    # BATCH_SIZE = 64

    objDetModelHelper.makeObjModelRank()

    # #from the way that data is divided into the folders: training/val/test: 80/10/10
    # return objDetModelHelper.makeImageModelScreen(x_train, y_train, x_validation, y_validation, modelPath, len(screenDict), EPOCHS, BATCH_SIZE)


# def testModel():
    # x_test, y_test = objDetModelHelper.getTestingData(testingDir, screenDict, num_rows, num_cols)
    # objDetModelHelper.testModel(x_test, y_test, modelPath, screenDict)


# Main function allows us to create and test our model seperately
if __name__ == '__main__':
    
    history = makeModel()

    # testModel()

    # Plot training & validation accuracy values
    # plt.figure(1)

    # plt.subplot(121)

    # plt.plot(history.history['accuracy'])
    # plt.plot(history.history['val_accuracy'])
    # plt.title('Model accuracy')
    # plt.ylabel('Accuracy')
    # plt.xlabel('Epoch')
    # plt.ylim(0,1)
    # plt.legend(['Train', 'Validation'], loc='upper left')

    # plt.subplot(122)

    # # Plot training & validation loss values
    # plt.plot(history.history['loss'])
    # plt.plot(history.history['val_loss'])
    # plt.title('Model loss')
    # plt.ylabel('Loss')
    # plt.xlabel('Epoch')
    # plt.legend(['Train', 'Validation'], loc='upper left')
    # plt.show()


    # plt.savefig(os.path.join(current_dir, 'diagnostics/'))