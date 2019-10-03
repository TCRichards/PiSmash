import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import numpy as np
from threading import Thread
from math import ceil

curDir = os.path.dirname(__file__)
trainingDir = os.path.join(curDir, 'trainingImages')

# Data Generator that distorts existing images and returns more data
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=[0.9, 1.25],
    horizontal_flip=True,
    fill_mode='nearest')


# Training Data paths and sizes
dataDirs = [os.path.join(trainingDir, x) for x in os.listdir(trainingDir)]
dirSizes = [len(os.listdir(dir)) for dir in dataDirs]
maxSize = max(dirSizes)


# Augments a random selection of images in the given directory until each category has roughly the same amount
def augment(dataDir):
    contents = os.listdir(dataDir)  # The names of each image
    size = len(contents)
    randomIdxs = np.random.randint(low=0, high=size, size=(maxSize - size))
    imgPaths = [os.path.join(dataDir, contents[idx]) for idx in randomIdxs]
    imgs = [load_img(imgPath) for imgPath in imgPaths]
    imgArrs = [img_to_array(img) for img in imgs]
    imgArrs = [img.reshape((1,) + img.shape) for img in imgArrs]
    batchesPerImg = ceil((maxSize - size) / size)
    for i, img in enumerate(imgArrs):
        print('File: {}\n'.format(imgPaths[i], dataDir))
        for batch in datagen.flow(img, batch_size=batchesPerImg,
                                  save_to_dir=dataDir,
                                  save_prefix=contents[i][:-4] + '_aug_{}'.format(i),
                                  save_format='png'):
            break


if __name__ == '__main__':
    for dataDir in dataDirs:
        Thread(target=augment, args=(dataDir, ), daemon=False).start()
