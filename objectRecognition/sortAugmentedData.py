'''
Utility file used to sort out augmented img files (from ScreenClassifier code) from training data
for object recognition models, so that images can be augmented AFTER labeling of bounding boxes 
Author: Nick Konz
Date Modified: 12/27/19
'''
import numpy as np
import argparse                  # allows us to deal with arguments to main()
from argparse import RawTextHelpFormatter
import sys
import os
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
current_dir = os.path.dirname(current_path)

def sortData(modelFolder):
    modelPath         = os.path.join(current_dir, modelFolder)

    trainImgFolderUnlabeledInclAugmentedPath = os.path.join(modelPath, "train_image_folder_unlabeled_include_augmented")

    trainImgFolderUnlabeledPath = os.path.join(modelPath, "train_image_folder_unlabeled")

    originPath = trainImgFolderUnlabeledInclAugmentedPath
    destPath = trainImgFolderUnlabeledPath

    count = 0
    for type in [name for name in os.listdir(originPath) if not name.startswith(".")]:
        # get name of file
        imgname = type

        # move file if not augmented
        if "aug" not in imgname:
            oldPath = os.path.join(originPath, imgname)
            newPath = os.path.join(destPath, imgname)
            os.rename(oldPath, newPath)
            count += 1

    print("%i images moved." % count)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("modelFolder",type=str)

    args              = parser.parse_args()
    modelFolder       = args.modelFolder
    
    sortData(modelFolder)