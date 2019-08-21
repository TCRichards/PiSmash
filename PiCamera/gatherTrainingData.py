import os
import picamera
from driveUpload import upload
import datetime
import time

curDir = os.path.dirname(__file__)
targetDir = os.path.join(curDir, 'trainingData')
maxCapacity = 100   # Total number of
total = 1e4         # Max out at 10,000 images
delay = 0.5         # Time between consecutive images


# Make the new directory if necessary
try:    # Attempt to create a new target directory
    os.mkdir(targetDir)
except FileExistsError:    # If the target directory already exists
    pass

# Setup the camera so that it auto-closes when finished
with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)  # Standard HD resolution
    i = 0
    while i < total:
        picNum = i % maxCapacity    # Modulo everything by the maximum capacity to only keep that many most recent images
        if picNum == 0:
            for img in os.listdir(targetDir):
                os.remove(os.path.join(os.path.dirname(__file__), img))

        imageName = datetime.datetime.now().strftime('pic_%m%d-%H:%M:%S_{}.png'.format(picNum))

        pathToImage = os.path.join(targetDir, imageName)
        time.sleep(delay)   # Time (s) between consecutive pictures
        camera.capture(pathToImage)
        upload(pathToImage)
        i += 1
