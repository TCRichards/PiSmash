# Need to create JSON files to capture video?
import vlc
import time

PiIPAddress = '192.168.0.100'               # Local address of my Raspberry Pi
streamURL = "rtsp://"+PiIPAddress+":8554/"  # URL over which the Pi streams video

# Capture the video using VLC.  OpenCV didn't work but that API is clearly superior
vlcInstance = vlc.Instance()
player = vlcInstance.media_player_new()
player.set_mrl(streamURL)
player.play()

i = 0
while (i < 1e3):
    picNum = i % 100
    time.sleep(0.1)
    player.video_take_snapshot(0, str(picNum)+'.snapshot.tmp.png', 0, 0)
