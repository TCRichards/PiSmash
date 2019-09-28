import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import numpy as np

curDir = os.path.dirname(__file__)
trainingDir = os.path.join(curDir, 'trainingImages')

datagen = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')


dataDirs = [os.path.join(trainingDir, x) for x in os.listdir(trainingDir)]
dirSizes = [len(os.listdir(dir)) for dir in dataDirs]
maxSize = max(dirSizes)

for i, dataDir in enumerate(dataDirs):
    contents = os.listdir(dataDir)
    size = dirSizes[i]
    randomIdxs = np.random.randint(low=0, high=size, size=(maxSize - size))
    imgPaths = [os.path.join(dataDir, contents[idx]) for idx in randomIdxs]
    imgs = [load_img(imgPath) for imgPath in imgPaths]
    imgArrs = [img_to_array(img) for img in imgs]
    imgArrs = [img.reshape((1,) + img.shape) for img in imgArrs]
    for i, img in enumerate(imgArrs):
        print('File: {}\n'.format(imgPaths[i], dataDir))
        datagen.flow(img, batch_size=size - maxSize,
                     save_to_dir=dataDir,
                     save_prefix=imgPaths[i] + '_aug_{}'.format(i),
                     save_format='jpeg')
