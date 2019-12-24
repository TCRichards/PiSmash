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

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("modelFolder",type=str)

    args              = parser.parse_args()
    modelFolder       = args.modelFolder
    modelPath         = os.path.join(current_dir, modelFolder)


    trainImgFolderUnlabeledPath = os.path.join(modelPath, "train_image_folder_unlabeled")
    validImgFolderUnlabeledPath = os.path.join(modelPath, "valid_image_folder_unlabeled")

    trainImgFolderPath = os.path.join(modelPath, "train_image_folder")
    validImgFolderPath = os.path.join(modelPath, "valid_image_folder")

    trainLabelFolderPath = os.path.join(modelPath, "train_annot_folder")
    validLabelFolderPath = os.path.join(modelPath, "valid_annot_folder")


    trainFileListUnlabeled = np.array([], dtype=str)          # List of filenames as str
    for path in [trainLabelFolderPath, validLabelFolderPath]:
        for type in [name for name in os.listdir(path) if not name.startswith(".")]:
            # get name of labeled file
            dataname = type.replace(".xml", "")
            imgname = dataname + ".png"
            # move file
            oldPath = os.path.join(trainImgFolderUnlabeledPath, imgname)
            newPath = os.path.join(trainImgFolderPath, imgname)
            os.rename(oldPath, newPath)