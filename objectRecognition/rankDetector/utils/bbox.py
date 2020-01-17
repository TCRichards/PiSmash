import numpy as np
import os
import cv2
from .colors import get_color


class BoundBox:
    def __init__(self, xmin, ymin, xmax, ymax, c = None, classes = None):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

        self.c       = c
        self.classes = classes

        self.label = -1
        self.score = -1

        self.playerRank = None


    def get_label(self):
        if self.label == -1:
            self.label = np.argmax(self.classes)

        return self.label

    def get_score(self):
        if self.score == -1:
            self.score = self.classes[self.get_label()]

        return self.score


def _interval_overlap(interval_a, interval_b):
    x1, x2 = interval_a
    x3, x4 = interval_b

    if x3 < x1:
        if x4 < x1:
            return 0
        else:
            return min(x2,x4) - x1
    else:
        if x2 < x3:
             return 0
        else:
            return min(x2,x4) - x3

def bbox_iou(box1, box2):
    intersect_w = _interval_overlap([box1.xmin, box1.xmax], [box2.xmin, box2.xmax])
    intersect_h = _interval_overlap([box1.ymin, box1.ymax], [box2.ymin, box2.ymax])

    intersect = intersect_w * intersect_h

    w1, h1 = box1.xmax-box1.xmin, box1.ymax-box1.ymin
    w2, h2 = box2.xmax-box2.xmin, box2.ymax-box2.ymin

    union = w1*h1 + w2*h2 - intersect

    return float(intersect) / union


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


def assignRank(numberString):
    switcher = {
        "first":    1,
        "second":   2,
        "third":    3,
        "fourth":   4,
        "fifth":    5,
        "sixth":    6,
        "seventh":  7
    }
    return switcher.get(numberString, None)


def rankBoxes(image, boxes, labels, obj_thresh, quiet=True):
    hitArray = np.zeros(len(boxes))     # Array will store a 1 if the box successfully classified, 0 otherwise

    for b, box in enumerate(boxes):
        for i in range(len(labels)):
            if box.classes[i] > obj_thresh: # If we're confident that this is the object
                hitArray[b] = 1             # Mark that this box had a valid result
                box.playerRank = assignRank(fixLabel(labels[i]))    # Assign the box with the proper rank
            if not quiet: print(box.playerRank)

    finalBoxes = []
    for i in range(len(hitArray)):
        if hitArray[i] == 1:
            finalBoxes.append(boxes[i])
    return finalBoxes


def draw_boxes(image, boxes, labels, obj_thresh, quiet=True):

    for box in boxes:
        label_str = ''
        label = -1

        for i in range(len(labels)):
            if box.classes[i] > obj_thresh:
                if label_str != '': label_str += ', '
                label_str += (fixLabel(labels[i]) + ' ' + str(round(box.classes[i]*100, 2)) + '%')
                label = i   # Index mapping to the correct location in fixLabel(labels)
            if not quiet: print(label_str)

        if label >= 0:
            text_size = cv2.getTextSize(label_str, cv2.FONT_HERSHEY_SIMPLEX, 1.1e-3 * image.shape[0], 5)
            width, height = text_size[0][0], text_size[0][1]
            region = np.array([[box.xmin-3,        box.ymin],
                               [box.xmin-3,        box.ymin-height-26],
                               [box.xmin+width+13, box.ymin-height-26],
                               [box.xmin+width+13, box.ymin]], dtype='int32')

            cv2.rectangle(img=image, pt1=(box.xmin,box.ymin), pt2=(box.xmax,box.ymax), color=get_color(label), thickness=5)
            cv2.fillPoly(img=image, pts=[region], color=get_color(label))
            cv2.putText(img=image,
                        text=label_str,
                        org=(box.xmin+13, box.ymin - 13),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1e-3 * image.shape[0],
                        color=(0,0,0),
                        thickness=2)

    return image
