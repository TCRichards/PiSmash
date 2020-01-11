'''
Utility file used to find which training object recognition images are labeled with bounding boxes,
and move these into the correct folder for a given object recognition model.
Used if not all training files have been labeled.
Author: Nick Konz
Date Modified: 12/23/19
'''
import numpy as np
import argparse                  # allows us to deal with arguments to main()
from argparse import RawTextHelpFormatter
import sys
import os
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
current_dir = os.path.dirname(current_path)


def moveLabeledData(modelFolder):
    modelPath         = os.path.join(current_dir, modelFolder)

    trainImgFolderUnlabeledPath = os.path.join(modelPath, "train_image_folder_unlabeled")
    validImgFolderUnlabeledPath = os.path.join(modelPath, "valid_image_folder_unlabeled")

    trainImgFolderPath = os.path.join(modelPath, "train_image_folder")
    validImgFolderPath = os.path.join(modelPath, "valid_image_folder")

    trainLabelFolderPath = os.path.join(modelPath, "train_annot_folder")
    validLabelFolderPath = os.path.join(modelPath, "valid_annot_folder")

    labelsPaths = [trainLabelFolderPath, validLabelFolderPath]
    oldPaths = [trainImgFolderUnlabeledPath, validImgFolderUnlabeledPath]
    newPaths = [trainImgFolderPath, validImgFolderPath]

    count = 0
    for i in range(2):
        labelpath = labelsPaths[i]
        for type in [name for name in os.listdir(labelpath) if not name.startswith(".")]:
            # get name of labeled file
            dataname = type.replace(".xml", "")
            imgname = dataname + ".png"

            # move file (if img hasn't been moved yet)
            oldPath = os.path.join(oldPaths[i], imgname)
            if os.path.exists(oldPath):
                newPath = os.path.join(newPaths[i], imgname)
                os.rename(oldPath, newPath)
                count += 1


    print("%i images moved." % count)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("modelFolder",type=str)

    args              = parser.parse_args()
    modelFolder       = args.modelFolder
    
    moveLabeledData(modelFolder)