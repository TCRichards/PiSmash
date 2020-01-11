'''
Uses screenshots of victory screen player ranking numbers to create a model to recognize
these numbers and rank players accordingly for a given match. Also used to test the model
individually.
Author: Nick Konz
Date Modified: 12/20/19
'''

import sys
import os
from inspect import getsourcefile
import matplotlib.pyplot as plt
from keras.models import load_model
from collections import OrderedDict

current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

if __name__ == '__main__':  # If we're running the file here, then imports are relative to here
    sys.path.insert(0, parent_dir)  # Add it
    import objDetModelHelper        # Import module from parent directory
else:   # If we're running the program from mainLoop, then paths are relative to project folder
    import objDetModelHelper
from collections import OrderedDict

trainingDir = os.path.join(current_dir, 'training_annot_folder')
validationDir = os.path.join(current_dir, 'valid_annot_folder')
testingDir = os.path.join(current_dir, 'test_image_folder')

# Image dimensions
# num_rows, num_cols = makeScreens.num_rows, makeScreens.num_cols

# modelPath = os.path.join(parent_dir, 'rankModel.h5')

# Translates screen type to an integer
rankDict = OrderedDict({
    "first": 0,
    "second": 1,
    "third": 2,
    "fourth": 3,
    "fifth": 4,
    "sixth": 5,
    "seventh": 6,
    "eighth": 7
})


#def trainModel(): # training is accomplished through experiencor's third party yolov3 training scripts.


# def testModel():
    # x_test, y_test = objDetModelHelper.getTestingData(testingDir, screenDict, num_rows, num_cols)
    # objDetModelHelper.testModel(x_test, y_test, modelPath, screenDict)

def testModel():
    model = load_model('rankModel.h5')
    for imgName in [name for name in os.listdir(testingDir) if not name.startswith(".")]:
        testImagePath = os.path.join(testingDir, imgName)
        # image, image_w, image_h = objDetModelHelper.getSingleTestingData(testImagePath)
        # objDetModelHelper.makePrediction(model, testImagePath)
        objDetModelHelper.detectRanks(testImagePath)


# Main function allows us to create and test our model seperately
if __name__ == '__main__':
    testModel()
