import keras
import vlc
import time

screenModelPath = 'screenModelPrototype.h5'
iconModelPath = 'iconModelPrototype.h5'

PiIPAddress = '192.168.0.100'               # Local address of my Raspberry Pi
streamURL = "rtsp://" + PiIPAddress + ":8554/"  # URL over which the Pi streams video


def captureVideo():
    # Capture the video using VLC.  OpenCV didn't work but that API is clearly superior
    vlcInstance = vlc.Instance()
    player = vlcInstance.media_player_new()
    player.set_mrl(streamURL)
    player.play()

    i = 0
    while (i < 1e3):
        picNum = i % 100
        time.sleep(0.1)
        player.video_take_snapshot(0, 'Screenshots/{}.snapshot.tmp.png'.format(picNum), 0, 0)
        i += 1


def main():
    screenModel = keras.load_model(screenModelPath)
    iconModel = keras.load_model(iconModelPath)
