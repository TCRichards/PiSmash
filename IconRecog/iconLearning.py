'''
Uses training images stored in directory to build neural network
Author: Thomas Richards
Date Modified: 5/20/19
'''

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from PIL import Image
import pathlib
import makeIcons

tf.logging.set_verbosity(tf.logging.ERROR) # Avoid annoying warnings

trainingDir = makeIcons.trainingDir
testingDir = makeIcons.testingDir
curDir = makeIcons.curDir
iconDir = makeIcons.iconDir

# Image dimensions
num_rows, num_cols = makeIcons.num_rows, makeIcons.num_cols

# Maps character names to corresponding labels for classification
characterDict = {
    "bayonetta" : 0,
    "bowser" : 1,
    "captainFalcon" : 2,
    "chrom" : 3,
    "cloud" : 4,
    "corin" : 5
}

# Identical to charcterDict, but with keys and values swapped
#labelDict = {v: k for k, v in characterDict.items()}

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
    newLabels = np.ones(trainingPics.size, dtype=np.uint8)*charValue        # Make a list of labels that is the proper length and value
    testLabelList = np.append(testLabelList, newLabels)

# Convert training data file paths to images
numTrainingFiles = len(trainFileList)
x_train = np.empty([numTrainingFiles, num_rows, num_cols]) # Make x_train an empty 3D array, where 1st dimension corresponds to image number
                                                    # Allows image indexing with only first index
for i in range(numTrainingFiles):
    newIm = Image.open(trainFileList[i]).convert('L')             # Convert the file name to a greyscale image
    newIm_array = np.array(newIm).astype(float)/255.         # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
    x_train[i] = newIm_array                                 # Stack the new image at the bottom of the training set

y_train = trainLabelList                                     # Refer to the labels as y_train for continuity

# Convert training data file paths to images
numTestingFiles = len(testFileList)
x_test = np.empty([numTestingFiles, num_rows, num_cols]) # Make x_train an empty 3D array, where 1st dimension corresponds to image number
                                                    # Allows image indexing with only first index
for i in range(numTestingFiles):
    newIm = Image.open(testFileList[i]).convert('L')         # Convert the file name to a greyscale image
    newIm_array = np.array(newIm).astype(float)/255.         # Convert greyscale image to a numpy array (num_rows x num_cols) and normalize
    x_test[i] = newIm_array                                  # Stack the new image at the bottom of the training set

y_test = trainLabelList                                     # Refer to the labels as y_test for continuity

# Convert matrices to 4D tensors
x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], x_train.shape[2], 1))
x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], x_test.shape[2], 1))
# Create CNN model=======================================================================

# Train the model!
EPOCHS = 10
BATCH_SIZE = 16

model = tf.keras.Sequential()
# Must define the input shape in the first layer of the neural network
model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=2, padding='same', activation='relu', input_shape=(200,200,1)))    #TODO: Not sure if this shape is correct
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.3))
model.add(tf.keras.layers.Conv2D(filters=32, kernel_size=2, padding='same', activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
model.add(tf.keras.layers.Dropout(0.3))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(10, activation='softmax'))
# Take a look at the model summary
#model.summary()

model.compile(loss='sparse_categorical_crossentropy',
             optimizer='adam',
             metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=64, epochs=10,verbose=1,validation_split=0.2)

# Save the model including architecture and weights in an h5 file
model.save('iconModelPrototype.h5')

# Evaluate how well the model did
score = model.evaluate(x_test, y_test, verbose=0)
#=============================================
''' I don't understand datasets, so use numpy arrays insted
# Convert numpy arrays into tensorflow constants
filenames = tf.constant(fileList)
labels = tf.constant(labelList)

# Create the data set
# Labels signify the desired classification for each image
dataset = tf.data.Dataset.from_tensor_slices((filenames, labels)) # Make into tensorflow dataset

# parse every image in the dataset using `map` -> converts string name to image
# Used to iterate over the entire dataset
def _parse_function(filename, label):
    image_string = tf.read_file(filename)
    image_decoded = tf.image.decode_jpeg(image_string, channels=1)
    image = tf.cast(image_decoded, tf.float32) / 255
    return image, label

dataset = dataset.map(_parse_function)
iterator = dataset.make_one_shot_iterator()
images, labels = iterator.get_next()

# Run the tensorflow session for every set of images and labels==========================
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(EPOCHS):
        try:
            nextImg, nextLbl = sess.run([images, labels])
            #_, loss_value = sess.run([images, labels])
            #print("Iter: {}, Loss: {:.4f}".format(i, loss_value))
        except tf.errors.OutOfRangeError:
            break

# Images are x_train, labels are y_train
'''
