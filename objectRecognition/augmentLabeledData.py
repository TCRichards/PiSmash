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
import os
from inspect import getsourcefile
import cv2
import xml.etree.ElementTree as ET

from kerasYOLO3 import parse_voc_annotation
from data_aug import Augmentation

current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
current_dir = os.path.dirname(current_path)

from objDetModelHelper import allLabels

minObjCount = 100 # minimum count of needed instances of each class


def getBoxesArrAndLabels(all_train_ints_element_obj): # returns the bounding boxes and corresponding labels for a single img
    boxes = []
    labels = []
    for box in all_train_ints_element_obj:
        labels.append(box['name'])
        boxes.append(np.array([box['xmin'],
                                box['ymin'],
                                box['xmax'],
                                box['ymax'],
        ]))

    return np.array(boxes), np.array(labels)

def getNewAugPath(imgpath, ind): # makes sure that multiple augmented images from same source image are labeled differently
    add = "_aug{}.jpeg".format(str(ind))
    augimgpath = imgpath.replace(".jpeg", add)
    if not os.path.exists(augimgpath):
        return augimgpath, ind
    else:
        return getNewAugPath(imgpath, ind + 1)

def augmentSingleImg(all_train_ints_element, labelPath):#augments a single image and saves the new augmented image and it's xml label file)
    boxes, labels = getBoxesArrAndLabels(all_train_ints_element['object'])
    #print(boxes, labels) 
    imgpath = all_train_ints_element['filename']
    imgfilename = os.path.basename(imgpath)
    img = cv2.imread(imgpath)

    # Do augmentation
    dataAug = Augmentation()
    auged_img, auged_bboxes, auged_labels = dataAug(img, boxes, labels)
    # auged_bbox = (xmin, ymin, xmax, ymax)

    # save augmented image
    augimgpath, newInd = getNewAugPath(imgpath, 0)
    cv2.imwrite(augimgpath, auged_img)

    #print(img.shape, auged_img.shape)
    # (720, 1280, 3) (917, 1379, 3)

    # make new xml file for augmented labels
    #print(auged_bboxes, auged_labels)
    # [[385 322 451 382], [647 288 712 355], [883 238 961 324]] 
    # ['second' 'third' 'first']
    xmlpath = os.path.join(labelPath, imgfilename.replace(".jpeg", ".xml"))
    tree = ET.parse(xmlpath)
    #print(str(ET.tostring(tree.getroot())))
    for elem in tree.iter():
            # modify all of the necessary tags from the unaugmented file
            # path
            if 'filename' in elem.tag:
                elem.text = os.path.basename(augimgpath)
            if 'path' in elem.tag:
                elem.text = augimgpath
            # img dims
            if 'size' in elem.tag:
                for attr in list(elem):
                    if 'width' in attr.tag:
                        attr.text = str(auged_img.shape[1])
                    if 'height' in attr.tag:
                        attr.text = str(auged_img.shape[0])
            labelsUsed = []
            labelInd = -1
            if 'object' in elem.tag or 'part' in elem.tag:
                for attr in list(elem):
                    if 'name' in attr.tag: # detect which label this object has
                        for i, aug_label in enumerate(auged_labels):
                            if attr.text == aug_label:
                                labelInd = i
                                labelsUsed.append(aug_label)

                    if 'bndbox' in attr.tag: # change bounding box coords to new
                        for dim in list(attr):
                            if 'xmin' in dim.tag:
                                dim.text = str(auged_bboxes[labelInd][0])
                            if 'ymin' in dim.tag:
                                dim.text = str(auged_bboxes[labelInd][1])
                            if 'xmax' in dim.tag:
                                dim.text = str(auged_bboxes[labelInd][2])
                            if 'ymax' in dim.tag:
                                dim.text = str(auged_bboxes[labelInd][3])

            # checks for labels that did not carry over to augmented images and deletes them
            root = tree.getroot()
            if 'object' in elem.tag or 'part' in elem.tag:
                for attr in list(elem):
                    if 'name' in attr.tag: # detect which label this object has
                        if attr.text not in labelsUsed: # if the label is only found in non-augmented image, not augmented
                            root.remove(elem)
                            print("a bounding box dissapeared upon augmentation")

    add = "_aug{}.xml".format(str(newInd))
    augxmlpath = xmlpath.replace(".xml", add)
    #print(str(ET.tostring(tree.getroot())))

    # save label file
    tree.write(augxmlpath)

    return

def augmentAndBalanceData(modelFolder):
    modelPath         = os.path.join(current_dir, modelFolder)
    imgPath = os.path.join(modelPath, "train_image_folder/")
    labelPath = os.path.join(modelPath, "train_annot_folder/")


    ###################

    all_train_ints, seen_train_labels = parse_voc_annotation(labelPath, imgPath, allLabels, ignoreAugmented=True) #These args are the same as in config.json
    # ^ all non-augmented training instances
    all_train_ints_inclAug, seen_train_labels_inclAug = parse_voc_annotation(labelPath, imgPath, allLabels)
    # ^ ALL instances, including augmented

    labelsCounts = {lbl : 0 for lbl in allLabels} # ~ {num of label1 objects, num of label2 objects, ... etc} for entire training set
    labelsCountsInclAug = {lbl : 0 for lbl in allLabels} 

    for all_train_ints_element in all_train_ints: # examine the population of class labels for the whole training set
        imgLabels = list(getBoxesArrAndLabels(all_train_ints_element['object'])[1])
        for lbl in imgLabels:
            labelsCounts[lbl] += 1

    for all_train_ints_element in all_train_ints_inclAug: # examine the population of class labels for the whole training set
        imgLabels = list(getBoxesArrAndLabels(all_train_ints_element['object'])[1])
        for lbl in imgLabels:
            labelsCountsInclAug[lbl] += 1

    print("Total number of labels before new augmentation: \n", labelsCountsInclAug, "\n")
    print("Total number of non-augmented labels before new augmentation: \n", labelsCounts, "\n")

    ###################

    # Balance the dataset via augmentation:
    # Begin by making sure that each class has at least 100 examples (including augmented)
    for label in allLabels:
        if labelsCountsInclAug[label] < minObjCount: # augments images that have this label until 100 instances of this underrepresented class is reached. prioritizes augmented images with fewer objects.
            nonAugObjCount = labelsCounts[label]
            lowTrainInts = [trainInt for trainInt in all_train_ints if label in list(getBoxesArrAndLabels(trainInt['object'])[1])]
            # ^ list of train instances that have this low-represented class
            lowTrainIntLabelLists = [list(getBoxesArrAndLabels(trainInt['object'])[1]) for trainInt in all_train_ints if label in list(getBoxesArrAndLabels(trainInt['object'])[1])]
            # ^ their corresponding label lists
            lowTrainIntLabelCounts = [len(lblList) for lblList in lowTrainIntLabelLists]
            # ^ the number of labels in each of them

            sortedLowTrainInts = [x for _, x in sorted(zip(lowTrainIntLabelCounts, lowTrainInts), key=lambda pair: pair[0])]
            # ^ list of train instances that have this low-represented class, sorted with number of labels increasing
            sortedLowTrainIntLabelLists = [list(getBoxesArrAndLabels(trainInt['object'])[1]) for trainInt in sortedLowTrainInts if label in list(getBoxesArrAndLabels(trainInt['object'])[1])]
            # ^ list of corresponding labels


            ct = nonAugObjCount # running total number of training data that have this class, INCLUDING augmented.
            i = 0 # index used to loop over available non-augmented training data
            #print(len(sortedLowTrainInts))
            while ct < minObjCount:
                #print(ct - nonAugObjCount, nonAugObjCount - 1)
                i = (( ct - nonAugObjCount ) % (nonAugObjCount - 1) )
                
                #print(i, ct, nonAugObjCount)
                augmentSingleImg(sortedLowTrainInts[i], labelPath)


                for lbl in sortedLowTrainIntLabelLists[i]: # updates count
                    labelsCountsInclAug[lbl] += 1

                i += 1
                ct += 1
            

    
    print("Total number of labels after augmentation: \n", labelsCountsInclAug, "\n")

    ###################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("modelFolder",type=str)

    args              = parser.parse_args()
    modelFolder       = args.modelFolder

    augmentAndBalanceData(modelFolder)