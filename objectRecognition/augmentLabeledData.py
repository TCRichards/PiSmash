'''
Augments XML VOC labeled object recognition data (both the images and their corresponding bounding boxes),
so that augmented don't need to be manually labeled. Doesn't use keras' generator methods, as these don't
directly support bounding box-labeled images.
Code thanks to: https://github.com/lele12/object-detection-data-augmentation
Author: Nick Konz
Date: 12/27/2019
'''

# parses labeled training img folder and training img annots folder and augments un-augmented images.
# should it also autobalance augmentation such that all classes represented equally?
# idea: prioritize augmented images that have higher-numbered labeled

import numpy as np
import argparse                  # allows us to deal with arguments to main()
from argparse import RawTextHelpFormatter
import sys
import os
from inspect import getsourcefile
import cv2
import copy
from numpy import random
import xml.etree.ElementTree as ET
import pickle
import collections

current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
current_dir = os.path.dirname(current_path)
from objDetModelHelper import allLabels
labels = allLabels

from kerasYOLO3 import parse_voc_annotation
from data_aug import Augmentation

def getBoxesArrAndLabels(all_train_ints_element):
    boxes = []
    labels = []
    for box in all_train_ints_element:
        labels.append(box['name'])
        boxes.append(np.array([box['xmin'],
                                box['ymin'],
                                box['xmax'],
                                box['ymax'],
        ]))

    return np.array(boxes), np.array(labels)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("modelFolder",type=str)

    args              = parser.parse_args()
    modelFolder       = args.modelFolder

    modelPath         = os.path.join(current_dir, modelFolder)
    imgPath = os.path.join(modelPath, "train_image_folder/")
    labelPath = os.path.join(modelPath, "train_annot_folder/")

    all_train_ints, seen_train_labels = parse_voc_annotation(labelPath, imgPath, labels) #These args are the same as in config.json
    print(all_train_ints)

    boxes, labels = getBoxesArrAndLabels(all_train_ints[0]['object'])
    print(boxes, labels) 
    filename = all_train_ints[0]['filename']

    # img = cv2.imread(filename)
    img = cv2.imread(filename)
    dataAug = Augmentation()
    auged_img, auged_bboxes, auged_labels = dataAug(img, boxes, labels)