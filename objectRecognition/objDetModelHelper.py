'''
This program is used to define object recognition neural networks, using the YOLOv3 model,
including code that assists with image and bounding box conversion.
Used to call these models for predictions.
Based on https://github.com/experiencor/keras-yolo3
Author: Nick Konz
'''
import argparse
import os
import numpy as np
from PIL import Image, ImageFile
from collections import OrderedDict
from keras.layers import Conv2D, Input, BatchNormalization, LeakyReLU, ZeroPadding2D, UpSampling2D
from keras.layers.merge import add, concatenate
from keras.models import Model, load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import struct
import cv2
from inspect import getsourcefile
import matplotlib.pyplot as pyplot
from matplotlib.patches import Rectangle

from kerasYOLO3 import *

# np.set_printoptions(threshold=np.nan)
# os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"]="0"

# argparser = argparse.ArgumentParser(
#     description='test yolov3 network with coco weights')

# argparser.add_argument(
#     '-w',
#     '--weights',
#     help='path to weights file')

# argparser.add_argument(
#     '-i',
#     '--image',
#     help='path to image file')

current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

rankDetectDir = os.path.join(current_dir, "rankDetector/")


# CONSTANTS
input_w, input_h = 416, 416 #fixed dimensions of neural network img inputs

# define the threshold for overlapping bounding boxes (see do_nms())
nms_thresh = 0.5

# define the probability threshold for detected objects
obj_thresh = 0.6

# define the anchors; ``average'' dimensions of bounding boxes found in training set
# this is like a starting guess for the bounding box anchors
# found with gen_anchors.py with experiencor's keras-yolo3
anchors = [12,22, 12,30, 14,26, 15,37, 15,21, 16,31, 17,26, 19,34, 19,44]

# define the labels
allLabels = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh"] #, "eighth"]

# DATA HANDLING

def getTrainingData(trainingDir, classDict, num_rows, num_cols):
    # Create empty numpy arrays to store file names and corresponding labels
    trainFileList = np.array([], dtype=str)          # List of filenames as str
    trainLabelList = np.array([], dtype=int)

    # Get training file paths and labels
    for type in [name for name in os.listdir(trainingDir) if not name.startswith(".")]: # The list comprehension excludes ``hidden'' files (which appeared when running on a mac).                    # List all character directories
        trainImageDir = trainingDir + type + '/'                  # Folder containing this character's images
        trainingPics = np.array([name for name in os.listdir(trainImageDir) if not name.startswith(".")])            # Name of each image in the directory

        for i in range(len(trainingPics)):
            trainImagePath = trainImageDir + trainingPics[i]
            trainFileList = np.append(trainFileList, trainImagePath)             # Inefficient to append at each iteration, but this was hard

        value = classDict.get(type)
        newLabels = np.ones(trainingPics.size, dtype=np.uint8) * value          # Make a list of labels that is the proper length and value
        trainLabelList = np.append(trainLabelList, newLabels)

    # Convert training data file paths to images
    numTrainingFiles = len(trainFileList)
    x_train = np.empty([numTrainingFiles, num_rows, num_cols, 3])   # Make x_train an empty 3D array, where 1st dimension corresponds to image number

    for i in range(numTrainingFiles):
        rawIm = Image.open(trainFileList[i])
        newIm = rawIm.resize((num_rows, num_cols))                  # Rescale the image to num_rows x num_cols
        newIm_array = np.array(newIm)[:, :, :3].astype(float) / 255.          # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
        x_train[i] = newIm_array                                    # Stack the new image at the bottom of the training set
    y_train = trainLabelList                                        # Refer to the labels as y_train for continuity
    return x_train, y_train


def getSingleTestingData(image_path):
    # TESTING WITH ONE IMG:
    # load and prep image for keras
    image, image_w, image_h = load_image_pixels(image_path, (input_w, input_h))

    return image, image_w, image_h

# rank object detector initial model constructor
# def buildUntrainedModelRank():
#     # define model
#     model = make_yolov3_model()

#     # load model weights
#     weightsPath = os.path.join(parent_dir, 'objectRecognition/yolov3.weights')
#     weight_reader = WeightReader(weightsPath)

#     # load weights into model
#     weight_reader.load_weights(model)

#     model.save('rankModel.h5')

# TESTING/PREDICTING
def fixLabel(label_str): #code I added to fix mislabeling
    # if len(label_str) == 0:
    #     return label_str
    # else:
    #     short = label_str.split(" ")[0]
    switcher = {
        "first":    "fifth",
        "second":   "first",
        "third":    "fourth",
        "fourth":   "second",
        "fifth":    "seventh",
        "sixth":    "sixth",
        "seventh":  "third"
    }
    return switcher.get(label_str, None)

def makePrediction(infer_model, image_path):
    image = cv2.imread(image_path)

    # predict the bounding boxes
    boxes = get_yolo_boxes(infer_model, [image], input_h, input_w, anchors, obj_thresh, nms_thresh)[0]

    # fix mislabeling
    for box in boxes:
        box.label = fixLabel(box.label)

    return boxes


def rankToInt(rankStr):
    switcher = {
        "first":    1,
        "second":   2,
        "third":    3,
        "fourth":   4,
        "fifth":    5,
        "sixth":    6,
        "seventh":  7,
        "eighth":   8
    }
    return switcher.get(rankStr, None)

def detectRanks(image_path):
    model_dir = os.path.join(rankDetectDir, 'rankModel.h5')
    model = load_model(model_dir)
    image, image_w, image_h = getSingleTestingData(image_path)
    boxes = makePrediction(model, image, image_h, image_w, image_path)

    return boxes
