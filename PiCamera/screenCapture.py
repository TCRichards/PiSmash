import vlc
import os
import time
import datetime
import errno
from driveUpload import upload


def capture(videoSource, targetDir, maxCapacity=100, total=1000, delay=1, outputFormat='date', uploading=False):
    try:    # Attempt to create a new target directory
        os.mkdir(targetDir)
    except OSError as e:    # If the target directory already exists
        if e.errno != errno.EEXIST:
            raise

    # Clear the directory of old images
    for im in os.listdir(targetDir):
        os.remove(os.path.join(targetDir, im))

    # Capture the video using VLC.  OpenCV didn't work but that API is clearly superior
    vlcInstance = vlc.Instance()
    player = vlcInstance.media_player_new()
    player.set_mrl(videoSource)
    player.play()

    i = 0
    while i < total:
        picNum = i % maxCapacity    # Modulo everything by the maximum capacity to only keep that many most recent images
        # import pdb
        # pdb.set_trace()
        if outputFormat == 'number':
            label = 'shot_{}.png'.format(picNum)
        else:
            label = datetime.datetime.now().strftime('shot_%m_%d_{}.png'.format(picNum))

        label = os.path.join(targetDir, label)
        time.sleep(delay)     # 0.3 seconds between image
        result = player.video_take_snapshot(0, label, 0, 0)
        i += 1
        if result > 0:
            print('captured shot {}'.format(picNum))
        if uploading:
            upload(label)


if __name__ == '__main__':
    targetDir = os.path.join(os.path.dirname(__file__), 'testShots')
    videoSource = os.path.join(os.path.dirname(__file__), 'Videos/sampleVid1.MOV')
    capture(videoSource, targetDir, outputFormat='date', uploading=True)
