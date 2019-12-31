'''
Utility file used to convert png filenames to jpegs in xml label files
Author: Nick Konz
Date Modified: 12/30/19
'''
import numpy as np
import argparse                  # allows us to deal with arguments to main()
from argparse import RawTextHelpFormatter
import sys
import os
from inspect import getsourcefile
import xml.etree.ElementTree as ET

current_path = os.path.abspath(getsourcefile(lambda: 0))    # Add parent directory to the path
current_dir = os.path.dirname(current_path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("modelFolder",type=str)

    args              = parser.parse_args()
    modelFolder       = args.modelFolder
    
    modelPath         = os.path.join(current_dir, modelFolder)

    trainLabelFolderPath = os.path.join(modelPath, "train_annot_folder")
    validLabelFolderPath = os.path.join(modelPath, "valid_annot_folder")

    labelsPaths = [trainLabelFolderPath, validLabelFolderPath]

    count = 0
    for i in range(2):
        labelpath = labelsPaths[i]
        for typ in [name for name in os.listdir(labelpath) if not name.startswith(".")]:
            # get name of labeled file
            labelname = typ
            xmlfilename = os.path.join(labelpath, labelname)
            tree = ET.parse(xmlfilename)
            ct = False
            for elem in tree.iter():
                if 'filename' in elem.tag:
                    if "png" in elem.text:
                        text = elem.text
                        text = text.replace('png', 'jpeg')
                        elem.text = text
                        ct = True
                if 'path' in elem.tag:
                    if "png" in elem.text:
                        text = elem.text
                        text = text.replace('png', 'jpeg')
                        elem.text = text
                        ct = True
            if ct:
                count += 1
            tree.write(xmlfilename)
            


    print("%i xmls converted." % count)