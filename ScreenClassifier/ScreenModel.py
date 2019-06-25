'''
Uses screenshots from gameplay to make a model that classifies a game in one of three categories
Author: Thomas Richards
Date Modified: 6/24/19
'''

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from PIL import Image
import pathlib
import makeScreens
from collections import OrderedDict

tf.logging.set_verbosity(tf.logging.ERROR) # Avoid annoying warnings

trainingDir = makeScreens.trainingDir
testingDir = makeScreens.testingDir

# Image dimensions
num_rows, num_cols = makeScreens.num_rows, makeScreens.num_cols

modelName = 'screenModelPrototype.h5'

# Translates screen type to an integer
screenDict = OrderedDict({
    "Select" : 0,
    "Game" : 1,
    "Victory" : 2
    })

# Create empty numpy arrays to store file names and corresponding labels
trainFileList = np.array([], dtype = str)                       # List of filenames as str
trainLabelList = np.array([], dtype = int)

testFileList = np.array([], dtype = str)                        # List of filenames as str
testLabelList = np.array([], dtype = int)

# Get training file paths and labels
for screenType in os.listdir(trainingDir):                     # List all character directories
    trainImageDir = trainingDir+'/'+screenType+'/'                  # Folder containing this character's images
    trainingPics = np.array(os.listdir(trainImageDir))            # Name of each image in the directory

    for i in range(len(trainingPics)):
        trainImagePath = trainImageDir + trainingPics[i]
        trainFileList = np.append(trainFileList, trainImagePath)             # Inefficient to append at each iteration, but this was hard

    screenValue = screenDict.get(screenType)
    newLabels = np.ones(trainingPics.size, dtype=np.uint8)*screenValue        # Make a list of labels that is the proper length and value
    trainLabelList = np.append(trainLabelList, newLabels)

# Do the exact same thing for getting testing data
for screenName in os.listdir(testingDir):                     # List all character directories
    testImageDir = testingDir+'/'+screenName+'/'                  # Folder containing this character's images
    testingPics = np.array(os.listdir(testImageDir))            # Name of each image in the directory

    for i in range(len(testingPics)):
        testImagePath = testImageDir + testingPics[i]
        testFileList = np.append(testFileList, testImagePath)             # Inefficient to append at each iteration, but this was hard

    screenValue = screenDict.get(screenName)
    newLabels = np.ones(testingPics.size, dtype=np.uint8)*screenValue        # Make a list of labels that is the proper length and value
    testLabelList = np.append(testLabelList, newLabels)


# Convert training data file paths to images
numTrainingFiles = len(trainFileList)
x_train = np.empty([numTrainingFiles, num_rows, num_cols, 3]) # Make x_train an empty 3D array, where 1st dimension corresponds to image number
                                                              # Allows image indexing with only first index
for i in range(numTrainingFiles):
    rawIm = Image.open(trainFileList[i])
    newIm = rawIm.resize((num_rows, num_cols))      # Rescale the image to num_rows x num_cols
    newIm_array = np.array(newIm).astype(float)/255.          # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
    x_train[i] = newIm_array                                  # Stack the new image at the bottom of the training set

y_train = trainLabelList                                      # Refer to the labels as y_train for continuity

# Convert training data file paths to images
numTestingFiles = len(testFileList)
x_test = np.empty([numTestingFiles, num_rows, num_cols, 3]) # Make x_train an empty 3D array, where 1st dimension corresponds to image number
                                                            # Allows image indexing with only first index
for i in range(numTestingFiles):
    rawIm = Image.open(testFileList[i])
    newIm = rawIm.resize((num_rows, num_cols))      # Rescale the image to num_rows x num_cols
    x_test[i] = newIm_array                                  # Stack the new image at the bottom of the training set

y_test = testLabelList                                       # Refer to the labels as y_test for continuity


# Convert matrices to 4D tensors
#x_train = x_train.reshape((1,) + x_train.shape)
#x_test = x_test.reshape((1,) + x_test.shape)
# Create CNN model=======================================================================

def makeModel():
    # Train the model!
    EPOCHS = 4
    BATCH_SIZE = 32

    # Make a sequential neural network
    model = tf.keras.Sequential()
    # Must define the input shape in the first layer of the neural network
    model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=2, padding='same', activation='relu', input_shape=(num_rows,num_cols,3)))    #TODO: Not sure if this shape is correct
    model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=2, padding='same', activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(256, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(len(screenDict), activation='softmax'))    # Final layer must have 1 node per character
    # Take a look at the model summary
    #model.summary()

    model.compile(loss='sparse_categorical_crossentropy',
                 optimizer='adam',
                 metrics=['accuracy'])

    history = model.fit(x_train, y_train, epochs=EPOCHS,verbose=1,validation_split=0.2)

    # Save the model including architecture and weights in an h5 file
    model.save(modelName) # Make sure model is including in .gitignore -- too large to push
    return history

def testModel():
    # Evaluate how well the model did
    model = tf.keras.models.load_model(modelName)
    score = model.evaluate(x_test, y_test, verbose=1) # Current model seems to suffer from overfitting -> goes from 96% acc to 78%
    print('Metrics tracked are: ' + str(model.metrics_names))
    print('Loss = ' + str(score[0]))
    print('Accuracy = ' + str(score[1]))
    # Look at specific predictions for random guesses
    guessNum = np.random.randint(0, len(x_test))
    randomX = x_test[guessNum].reshape((1,) + x_test[guessNum].shape)
    randomY = y_test[guessNum]
    plt.imshow(randomX[0,:,:,:])
    probs = model.predict(randomX)[0,:]     # Initial shape is (1, #possibilities)
    names = screenDict.keys()
    probDict = OrderedDict(sorted(zip(names, probs), reverse=True))
    print(probDict)

    plt.show()


def main(): # Main function allows us to create and test our model seperately
    makeModel()
    #testModel()



main()
#=============================================
