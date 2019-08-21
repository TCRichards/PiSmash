import os
import picamera
from driveUpload import upload
import datetime
import time
import socket
import errno


curDir = os.path.dirname(__file__)
targetDir = os.path.join(curDir, 'trainingData')
maxCapacity = 100   # Total number of
total = 1e4         # Max out at 10,000 images
delay = 0.5         # Time between consecutive images


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
while time.time() < startTime + 10:
    foundWifi = hasWifi()
    if foundWifi:
        break

if foundWifi:   # Only begin the stream if wifi is detected
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
                    os.remove(os.path.join(os.path.dirname(__file__), img))

            imageName = datetime.datetime.now().strftime('pic_%m%d-%H%M%S_{}.png'.format(picNum))

            pathToImage = os.path.join(targetDir, imageName)
            time.sleep(delay)   # Time (s) between consecutive pictures
            camera.capture(pathToImage)
            upload(pathToImage)
            i += 1
