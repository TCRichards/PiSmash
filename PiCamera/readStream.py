import vlc
import os
import time

PiIPAddress = '192.168.0.103'                   # Local address of my Raspberry Pi
streamURL = "rtsp://" + PiIPAddress + ":8554/"  # URL over which the Pi streams video

curDir = os.path.dirname(__file__)
imageDir = os.path.join(curDir, 'screenShots/')


def stream():
    # Clear the directory of old images
    for im in os.listdir(imageDir):
        os.remove(imageDir + im)

    # Capture the video using VLC.  OpenCV didn't work but that API is clearly superior
    vlcInstance = vlc.Instance()
    player = vlcInstance.media_player_new()
    player.set_mrl(streamURL)
    player.play()

    i = 0
    while (i < 1e3):
        picNum = i % 100    # Modulo everything by 100 to only keep 100 most recent images
        time.sleep(0.3)     # 0.3 seconds between image
        result = player.video_take_snapshot(0, imageDir + 'shot_{}.png'.format(picNum), 0, 0)
        i += 1
        if result > 0:
            print('captured shot {}'.format(picNum))


if __name__ == '__main__':
    stream()
