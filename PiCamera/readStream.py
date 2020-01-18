import vlc
import os
import time
import sys

# Create interface to easily edit the IP address on launch?
PiIPAddress = '192.168.0.26'                   # Local address of my Raspberry Pi
streamURL = "rtsp://" + PiIPAddress + ":8554/"  # URL over which the Pi streams video

curDir = os.path.dirname(__file__)
imageDir = os.path.join(curDir, 'screenShots/')


# General function that captures screenshe
def captureMedia(mediaPath, delay=0.3):
    # Clear the directory of old images
    for im in os.listdir(imageDir):
        os.remove(imageDir + im)

    # Capture the video using VLC.  OpenCV didn't work but that API is clearly superior
    vlcInstance = vlc.Instance()
    player = vlcInstance.media_player_new()
    player.set_mrl(mediaPath)
    """
    if sys.platform == "darwin": #necessary if run on a mac (DOESN'T WORK FOR NOW)
            from PyQt5 import QtCore
            from PyQt5 import QtGui
            from PyQt5 import QtWidgets

            vlcApp = QtWidgets.QApplication(sys.argv)
            vlcWidget = QtWidgets.QFrame()
            vlcWidget.resize(700,700)
            vlcWidget.show()
            player.set_nsobject(vlcWidget.winId())
    """
    player.play()

    i = 0
    while (i < 1e3):
        picNum = i % 100    # Modulo everything by 100 to only keep 100 most recent images
        time.sleep(delay)   # Time waited between image
        result = player.video_take_snapshot(0, imageDir + 'shot_{}.png'.format(picNum), 0, 0)
        i += 1
        if result > 0:
            print('captured shot {}'.format(picNum))


def captureStream():
    captureMedia(streamURL)


if __name__ == '__main__':
    captureStream()
