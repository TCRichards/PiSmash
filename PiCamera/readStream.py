# Need to create JSON files to capture video?
import vlc
import time

PiIPAddress = '192.168.0.103'                   # Local address of my Raspberry Pi
streamURL = "rtsp://" + PiIPAddress + ":8554/"  # URL over which the Pi streams video

if __name__ == '__main__':
    imageDir = '/PiCamera/screenShots/'
else:
    imageDir = 'PiCamera/screenShots/'


def stream():
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
