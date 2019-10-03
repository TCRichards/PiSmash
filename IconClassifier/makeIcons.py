'''
Uses character icons from Nintendo to generate a ton of training data
Author: Thomas Richards
Date Modified: 6/11/19
'''

import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array


# Paths
curDir = os.path.dirname(__file__)

trainingDir = os.path.join(curDir, 'trainingImages')
testingDir = os.path.join(curDir, 'testingImages')
validationDir = os.path.join(curDir, 'validationImages')
iconDir = os.path.join(curDir, 'rawIcons')

# Image dimensions
num_rows, num_cols = 200, 200

# Keras objectUsed to distort given images to generate more data
datagen = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')


def createTrainingData():
    # Take original images and distort, then store in player's directory
    for path in os.listdir(iconDir):
        if 'icon.png' in path:  # Only select icons
            img = load_img(iconDir + '/' + path)              # Create a PIL image using Keras's wrapper
            img = img.resize((num_rows, num_cols))            # Resize image dimensions
            img = img_to_array(img)                           # this is a Numpy array with shape (rows, columns, 3)
            img = img.reshape((1,) + img.shape)               # this is a Numpy array with shape (1, rows, columns, 3)

            charName = path[:-9]                              # Cut out the _icon.png suffix
# ================================================================================================
# Super interesting :\ create directories for training and testing data

            # If there is already a directory for this character, delete. Else, pass
            try:
                for file in os.listdir(trainingDir + '/' + charName):
                    os.remove(trainingDir + '/' + charName + '/' + file)
                os.rmdir(trainingDir + '/' + charName)
            except FileNotFoundError:
                pass
            os.mkdir(trainingDir + '/' + charName)  # Create a personal directory for each character

            # If there is already a directory for this character, delete. Else, pass
            try:
                for file in os.listdir(testingDir + '/' + charName):
                    os.remove(testingDir + '/' + charName + '/' + file)
                os.rmdir(testingDir + '/' + charName)
            except FileNotFoundError:
                pass
            os.mkdir(testingDir + '/' + charName)   # Create a personal directory for each character

# ===================================================================================================
# Then fill those directories with the images
            # Create training data
            i = 0
            for batch in datagen.flow(img, batch_size=1,
                                      save_to_dir=trainingDir + '/' + charName,
                                      save_prefix=charName + '_train',
                                      save_format='jpeg'):
                i += 1
                if i > 50:
                    break  # otherwise the generator would loop indefinitely

            # Eventually, testing data should be pictures captured from screen (different than training data), but for now use random changes to original
            # Create testing data
            i = 0
            for batch in datagen.flow(img, batch_size=1,
                                      save_to_dir=testingDir + '/' + charName,
                                      save_prefix=charName + '_trial',
                                      save_format='jpeg'):
                i += 1
                if i > 10:  # Only include 10 batches for testing
                    break   # otherwise the generator would loop indefinitely


if __name__ == '__main__':
    createTrainingData()
