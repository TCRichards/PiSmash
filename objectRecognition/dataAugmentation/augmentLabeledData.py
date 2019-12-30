'''
Augments XML VOC labeled object recognition data (both the images and their corresponding bounding boxes),
so that augmented don't need to be manually labeled. Doesn't use keras' generator methods, as these don't
directly support bounding box-labeled images.
Author: Nick Konz
Date: 12/27/2019
'''

# parses labeled training img folder and training img annots folder and augments un-augmented images.
# should it also autobalance augmentation such that all classes represented equally?
# idea: prioritize augmented images that have higher-numbered labeled