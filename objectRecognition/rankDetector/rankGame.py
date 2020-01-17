'''
Program adapted from https://github.com/experiencor/keras-yolo3
rankGame returns a list in oder of place in the game based on results from object detection
'''
import os
import argparse
import json
import cv2
import sys

try:
    from utils.utils import get_yolo_boxes, makedirs
    from utils.bbox import draw_boxes, rankBoxes
except ModuleNotFoundError:
    from .utils.utils import get_yolo_boxes, makedirs
    from .utils.bbox import draw_boxes, rankBoxes
from tqdm import tqdm
from keras.models import load_model
import numpy as np


curDir = os.path.dirname(__file__)
configPath = os.path.join(curDir, 'config.json')
modelPath = os.path.join(curDir, 'rankModel.h5')
outputPath = os.path.join(curDir, 'outputFolder/', 'annotedResults0.png')
imagePath = os.path.join(curDir, 'inputFolder/realResults0.png')


#
def rankGame(inputPath, draw_output=False):

    with open(configPath) as config_buffer:
        config = json.load(config_buffer)

    makedirs(outputPath)

    ###############################
    #   Set some parameter
    ###############################
    net_h, net_w = 416, 416 # a multiple of 32, the smaller the faster
    obj_thresh, nms_thresh = 0.5, 0.45

    ###############################
    #   Load the model
    ###############################
    os.environ['CUDA_VISIBLE_DEVICES'] = config['train']['gpus']
    infer_model = load_model(os.path.join(curDir, config['train']['saved_weights_name']))

    image = cv2.imread(inputPath)

    # predict the bounding boxes
    boxes = get_yolo_boxes(infer_model, [image], net_h, net_w, config['model']['anchors'], obj_thresh, nms_thresh)[0]
    # Sort boxes by x position sort in ascending player order
    sortedBoxes = sorted(boxes, key=lambda box: box.xmin)

    # draw bounding boxes on the image using labels
    if draw_output:
        draw_boxes(image, boxes, config['model']['labels'], obj_thresh)
        # write the image with bounding boxes to file
        # cv2.imwrite(outputPath.split('/')[-1], np.uint8(image))
        cv2.imshow('Annotated Image', image)
        cv2.waitKey(0)
    # Assign ranks to the boxes based on their labels
    rankedBoxes = rankBoxes(image, boxes, config['model']['labels'], obj_thresh)
    sortedRanks = [box.playerRank for box in rankedBoxes]
    return sortedRanks  # Returns a list of the integer ranks in order of ascending player number


if __name__ == '__main__':
    predict(imagePath)
