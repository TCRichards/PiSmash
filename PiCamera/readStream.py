import os
from screenCapture import capture

# Create interface to easily edit the IP address on launch?
PiIPAddress = '192.168.0.54'                   # Local address of my Raspberry Pi
streamURL = "rtsp://" + PiIPAddress + ":8554/"  # URL over which the Pi streams video

curDir = os.path.dirname(__file__)
imageDir = os.path.join(curDir, 'screenShots/')


def main():
    targetDir = os.path.join(os.path.dirname(__file__), 'screenShots')
    capture(streamURL, targetDir, outputFormat='number', delay=0.3)
