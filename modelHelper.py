'''
This program is the bread and butter of the machine learning.  Provides a template that
can be used by any classification program that gathers pre-generated training and testing data, and
makes a generic image classification model.
Author: Thomas Richards
'''

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from PIL import Image
import pathlib
from collections import OrderedDict

'''
Given a directory where training data is located, and a dictionary containing mappings between each
sub-directory name and classification label, this method outputs training data in numpy arrays
'''
def getTrainingData(trainingDir, myDict, num_rows, num_cols):
    # Create empty numpy arrays to store file names and corresponding labels
    trainFileList = np.array([], dtype = str)                       # List of filenames as str
    trainLabelList = np.array([], dtype = int)

    # Get training file paths and labels
    for type in os.listdir(trainingDir):                     # List all character directories
        trainImageDir = trainingDir+'/'+type+'/'                  # Folder containing this character's images
        trainingPics = np.array(os.listdir(trainImageDir))            # Name of each image in the directory

        for i in range(len(trainingPics)):
            trainImagePath = trainImageDir + trainingPics[i]
            trainFileList = np.append(trainFileList, trainImagePath)             # Inefficient to append at each iteration, but this was hard

        value = myDict.get(type)
        newLabels = np.ones(trainingPics.size, dtype=np.uint8)*value        # Make a list of labels that is the proper length and value
        trainLabelList = np.append(trainLabelList, newLabels)

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
    return x_train, y_train

def getTestingData(testingDir, myDict, num_rows, num_cols):
    testFileList = np.array([], dtype = str)                        # List of filenames as str
    testLabelList = np.array([], dtype = int)
    # Do the exact same thing for getting testing data
    for type in os.listdir(testingDir):                     # List all character directories
        testImageDir = testingDir+'/'+type+'/'                  # Folder containing this character's images
        testingPics = np.array(os.listdir(testImageDir))            # Name of each image in the directory

        for i in range(len(testingPics)):
            testImagePath = testImageDir + testingPics[i]
            testFileList = np.append(testFileList, testImagePath)             # Inefficient to append at each iteration, but this was hard

        value = myDict.get(type)
        newLabels = np.ones(testingPics.size, dtype=np.uint8)*value        # Make a list of labels that is the proper length and value
        testLabelList = np.append(testLabelList, newLabels)

    # Convert training data file paths to images
    numTestingFiles = len(testFileList)
    x_test = np.empty([numTestingFiles, num_rows, num_cols, 3]) # Make x_train an empty 3D array, where 1st dimension corresponds to image number
                                                                # Allows image indexing with only first index
    for i in range(numTestingFiles):
        rawIm = Image.open(testFileList[i])
        newIm = rawIm.resize((num_rows, num_cols))      # Rescale the image to num_rows x num_cols
        newIm_array = np.array(newIm).astype(float)/255.    # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
        x_test[i] = newIm_array                            # Stack the new image at the bottom of the training set

    y_test = testLabelList                                       # Refer to the labels as y_test for continuity
    return x_test, y_test

def makeImageModel(x_train, y_train, modelName, numTargets, EPOCHS, BATCH_SIZE):
    EPOCHS = 4
    BATCH_SIZE = 32
    num_rows, num_cols = len(x_train[1]), len(x_train[2])
    # Make a sequential neural network
    model = tf.keras.Sequential()
    # Create CNN model=======================================================================
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
    model.add(tf.keras.layers.Dense(numTargets, activation='softmax'))    # Final layer must have 1 node per character
    # Take a look at the model summary
    #model.summary()

    model.compile(loss='sparse_categorical_crossentropy',
                 optimizer='adam',
                 metrics=['accuracy'])

    history = model.fit(x_train, y_train, epochs=EPOCHS,verbose=1,validation_split=0.2)

    # Save the model including architecture and weights in an h5 file
    model.save(modelName) # Make sure model is included in .gitignore -- too large to push
    return history

def testModel(x_test, y_test, modelPath, matchDict):
    # Evaluate how well the model did
    model = tf.keras.models.load_model(modelPath)
    score = model.evaluate(x_test, y_test, verbose=1) # Current model seems to suffer from overfitting -> goes from 96% acc to 78%
    print('Metrics tracked are: ' + str(model.metrics_names))
    print('{} = {}'.format(model.metrics_names[0], score[0]))
    print('{} = {}'.format(model.metrics_names[1], score[1]))
    # Look at specific predictions for random guesses
    # Makes a figure showing 6 random images with pie charts giving top probabilities
    testFig = plt.figure()
    for i in range(0, 12, 2):
        testFig.add_subplot(2,6,i+1)
        guessNum = np.random.randint(0, len(x_test))
        randomX = x_test[guessNum].reshape((1,) + x_test[guessNum].shape)
        randomY = y_test[guessNum]
        plt.imshow(randomX[0,:,:,:])
        plt.axis('off')
        probs = model.predict(randomX)[0,:]     # Initial shape is (1, #possibilities)

        names = matchDict.keys()
        probDict = OrderedDict(sorted(zip(names, probs), key = lambda t: t[1], reverse=True)) # Place in an ordered dict to sort names along with probs
        keys = np.array(list(probDict.keys()))[:5]               # Extract ordered names and probabilities from ordered dict
        probabilities = np.array(list(probDict.values()))[:5]           # Keep maximum length of both to top 5 answers

        probLabels = []                                                 # Make fancy labels explaining probabilities
        for j in range(len(keys)):
            probLabels.append('{}: {:.2f} %'.format(keys[j], probabilities[j]*100))
        testFig.add_subplot(2,6,i+2)
        plt.pie(probabilities)
        plt.legend(loc=9, labels=probLabels, bbox_to_anchor=(0.5, 1.4), shadow=True, fancybox=True)
    plt.show()
