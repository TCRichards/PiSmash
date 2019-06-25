'''
Uses training images stored in directory to build neural network
Author: Thomas Richards
Date Modified: 6/18/19
'''

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from PIL import Image
import pathlib
import makeIcons
from collections import OrderedDict


tf.logging.set_verbosity(tf.logging.ERROR) # Avoid annoying warnings

trainingDir = makeIcons.trainingDir
testingDir = makeIcons.testingDir
curDir = makeIcons.curDir
iconDir = makeIcons.iconDir

# Image dimensions
num_rows, num_cols = makeIcons.num_rows, makeIcons.num_cols

modelName = 'iconModelPrototype.h5'

# Maps character names to corresponding labels for classification
characterDict = {
    "banjo&kazooie" : 0,
    "bayonetta" : 1,
    "bowser" : 2,
    "captainFalcon" : 3,
    "chrom" : 4,
    "cloud" : 5,
    "corin" : 6,
    "daisy" : 7,
    "darkPit" : 8,
    "darkSamus" : 9,
    "diddyKong" : 10,
    "donkeyKong" : 11,
    "drMario" : 12,
    "duckHunt" : 13,
    "falco" : 14,
    "fox" : 15,
    "ganondorf" : 16,
    "greninja" : 17,
    "hero" : 18,
    "iceClimbers" : 19,
    "ike" : 20,
    "incineroar" : 21,
    "inkling" : 22,
    "isabelle" : 23,
    "pokemonTrainer" : 24,
    "jigglypuff" : 25,
    "joker" : 26,
    "ken" : 27,
    "kingDedede" : 28,
    "kingKRool" : 29,
    "kirby" : 30,
    "link" : 31,
    "littleMac" : 32,
    "lucario" : 33,
    "lucas" : 34,
    "lucina" : 35,
    "luigi" : 36,
    "mario" : 37,
    "marth" : 38,
    "megaMan" : 39,
    "metaKnight" : 40,
    "mewtwo" : 41,
    "miiBrawler" : 42,
    "miiFighter" : 43,
    "miiGunner" : 44,
    "miiSwordfighter" : 45,
    "mrGame&Watch" : 46,
    "ness" : 47,
    "olimar" : 48,
    "pac-man" : 49,
    "palutena" : 50,
    "peach" : 51,
    "pichu" : 52,
    "pikachu" : 53,
    "piranhaPlant" : 54, # May need to include other color icons for this one
    "pit" : 55,
    "richter" : 56,
    "ridley" : 57,
    "ROB" : 58,
    "robin" : 59,
    "rosalina" : 60,
    "roy" : 61,
    "ryu" : 62,
    "samus" : 63,
    "sheik" : 64,
    "shulk" : 65,
    "simon" : 66,
    "snake" : 67,
    "sonic" : 68,
    "toonLink" : 69,
    "villager" : 70,
    "wario" : 71,
    "wiiFitTrainer" : 72,
    "wolf" : 73,
    "yoshi" : 74,
    "youngLink" : 75,
    "zelda" : 76,
    "zeroSuitSamus" : 77
}

# Identical to charcterDict, but with keys and values swapped
labelDict = {v: k for k, v in characterDict.items()}

# Create empty numpy arrays to store file names and corresponding labels
trainFileList = np.array([], dtype = str)                        # List of filenames as str
trainLabelList = np.array([], dtype = int)

testFileList = np.array([], dtype = str)                        # List of filenames as str
testLabelList = np.array([], dtype = int)

# Get training file paths and labels
for charName in os.listdir(trainingDir):                     # List all character directories
    trainImageDir = trainingDir+'/'+charName+'/'                  # Folder containing this character's images
    trainingPics = np.array(os.listdir(trainImageDir))            # Name of each image in the directory

    for i in range(len(trainingPics)):
        trainImagePath = trainImageDir + trainingPics[i]
        trainFileList = np.append(trainFileList, trainImagePath)             # Inefficient to append at each iteration, but this was hard

    charValue = characterDict.get(charName)
    newLabels = np.ones(trainingPics.size, dtype=np.uint8)*charValue        # Make a list of labels that is the proper length and value
    trainLabelList = np.append(trainLabelList, newLabels)

# Do the exact same thing for getting testing data
for charName in os.listdir(testingDir):                     # List all character directories
    testImageDir = testingDir+'/'+charName+'/'                  # Folder containing this character's images
    testingPics = np.array(os.listdir(testImageDir))            # Name of each image in the directory

    for i in range(len(testingPics)):
        testImagePath = testImageDir + testingPics[i]
        testFileList = np.append(testFileList, testImagePath)             # Inefficient to append at each iteration, but this was hard

    charValue = characterDict.get(charName)
    newLabels = np.ones(testingPics.size, dtype=np.uint8)*charValue        # Make a list of labels that is the proper length and value
    testLabelList = np.append(testLabelList, newLabels)


# Convert training data file paths to images
numTrainingFiles = len(trainFileList)
x_train = np.empty([numTrainingFiles, num_rows, num_cols, 3]) # Make x_train an empty 3D array, where 1st dimension corresponds to image number
                                                              # Allows image indexing with only first index
for i in range(numTrainingFiles):
    newIm = Image.open(trainFileList[i])                      # Convert the file name to a greyscale image
    newIm_array = np.array(newIm).astype(float)/255.          # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
    x_train[i] = newIm_array                                  # Stack the new image at the bottom of the training set

y_train = trainLabelList                                      # Refer to the labels as y_train for continuity

# Convert training data file paths to images
numTestingFiles = len(testFileList)
x_test = np.empty([numTestingFiles, num_rows, num_cols, 3]) # Make x_train an empty 3D array, where 1st dimension corresponds to image number
                                                    # Allows image indexing with only first index
for i in range(numTestingFiles):
    newIm = Image.open(testFileList[i])                      # Convert the file name to a greyscale image
    newIm_array = np.array(newIm).astype(float)/255.         # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
    x_test[i] = newIm_array                                  # Stack the new image at the bottom of the training set

y_test = testLabelList                                     # Refer to the labels as y_test for continuity


# Convert matrices to 4D tensors
#x_train = x_train.reshape((1,) + x_train.shape)
#x_test = x_test.reshape((1,) + x_test.shape)
# Create CNN model=======================================================================

def makeModel():
    # Train the model!
    EPOCHS = 75
    BATCH_SIZE = 32

    # Make a sequential neural network
    model = tf.keras.Sequential()
    # Must define the input shape in the first layer of the neural network
    model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=2, padding='same', activation='relu', input_shape=((num_rows,num_cols,3))))    #TODO: Not sure if this shape is correct
    model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=2, padding='same', activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(256, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(len(y_train), activation='softmax'))    # Final layer must have 1 node per character
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

    probs = model.predict(randomX)[0,:]  # Initial shape is (1, #possibilities)
    names = screenDict.keys()
    probDict = OrderedDict(sorted(zip(names, probs), reverse=True))
    print(probDict)


def main(): # Main function allows us to create and test our model seperately
    #makeModel()
    testModel()



main()
#=============================================
