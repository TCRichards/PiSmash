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
from keras.models import load_model

current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

if __name__ == '__main__':  # If we're running the file here, then imports are relative to here
    sys.path.insert(0, parent_dir)  # Add it
    import objDetModelHelper              # Import module from parent directory
else:   # If we're running the program from mainLoop, then paths are relative to project folder
    import objDetModelHelper


def trainModel():

    # load yolov3 model
    model = load_model('rankModel.h5')


def testModel():
    image_filename = 'zebra.jpg'
    
    model = load_model('rankModel.h5')
    image, image_w, image_h = objDetModelHelper.getTestingData(image_filename)
    objDetModelHelper.makePrediction(model, None, image, image_h, image_w, image_filename)

# Main function allows us to create and test our model seperately
if __name__ == '__main__':
    

    testModel()
