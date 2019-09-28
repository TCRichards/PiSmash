import os
import picamera
import datetime
import time
import socket
import errno
import sys


def hasWifi():
    testURL = 'www.google.com'      # The address is meaningless, just need to connect to something
    try:
        host = socket.gethostbyname(testURL)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except socket.gaierror:         # Error thrown if there's no Wifi
        return False


# Look for a wifi connection for up to 10 seconds
startTime = time.time()
foundWifi = False
while time.time() < startTime + 30:
    foundWifi = hasWifi()
    if foundWifi:
        break

# If we haven't found wifi after 30 seconds, give up
if not foundWifi:
    sys.exit(1)

# Needed to wait until connected to wifi in order to import
from googleDrive import upload


curDir = '/home/pi/PiSmash/PiCamera/'
targetDir = os.path.join(curDir, 'trainingData')
maxCapacity = 100   # Total number of
total = 1e5         # Max out at 100,000 images in a row
delay = 0.1         # Time between consecutive images


# Make the new directory if necessary
try:
    os.mkdir(targetDir)
except OSError as e:
    if e.errno == errno.EEXIST:
        print('Directory not created.')
else:
    raise

# Setup the camera so that it auto-closes when finished
with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)  # Standard HD resolution
    i = 0
    while i < total:
        picNum = i % maxCapacity    # Modulo everything by the maximum capacity to only keep that many most recent images
        if picNum == 0:
            for img in os.listdir(targetDir):
                os.remove(os.path.join(targetDir, img))

        imageName = datetime.datetime.now().strftime('pic_%m%d-%H%M%S_{}.png'.format(picNum))

        pathToImage = os.path.join(targetDir, imageName)
        time.sleep(delay)   # Time (s) between consecutive pictures
        camera.capture(pathToImage)
        upload(pathToImage)
        i += 1
