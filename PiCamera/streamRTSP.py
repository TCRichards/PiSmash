'''
Raspberry Pi script that initiates RTSP streaming completely contained within Python
Tests for wifi connection and begins streaming if detected within 10 secs in order to give time for
boot to complete
Author: Thomas Richards
Date Modified: 7/29/2019
'''

import subprocess
import socket
import time

curDir = '/home/pi/PiSmash/PiCamera/'   # Absolute path to program


def hasWifi():
    testURL = 'www.google.com'      # The address is meaningless, just need to connect to something
    try:
        host = socket.gethostbyname(testURL)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except socket.gaierror:         # Error thrown if there's no Wifi
        return False


if __name__ == '__main__':

    # Look for a wifi connection for up to 10 seconds
    startTime = time.time()
    foundWifi = False
    while time.time() < startTime + 10:
        foundWifi = hasWifi()
        if foundWifi:
            break

    if foundWifi:   # Only begin the stream if wifi is detected
        # create two files to hold the output and errors, respectively
        with open(curDir + 'streamLogs.txt', 'w+') as logs:    # Errors (although everything from streaming is interpreted as an error)
            firstCommand = subprocess.Popen(    # I have no idea wtf this does but it works!
                ["""cvlc -vvv v4l2c:///dev/video0:width=1280:height=720:chroma=H264 --sout '#rtp{sdp=rtsp://:8554/}' --demux h264"""],
                stderr=logs, shell=True)
            try:
                firstCommand.communicate(timeout=1)  # Executes the command and times out after 5 secs
            except subprocess.TimeoutExpired:   # Kill the first command after 5 secs and launch the second
                print('First Command Timed Out (Intentional) Beginning Second Command')
                firstCommand.kill()

                print('Successfully Began Stream')
                secondCommand = subprocess.Popen(
                    ["""dd if=/dev/video0 bs=1M | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' --demux=h264"""],
                    stderr=logs, shell=True)
                secondCommand.communicate()  # Don't force this one to end

            print('Stream Crashed')
            # reset file to read from it
            logs.seek(0)
            # save all stream outputs
            errors = logs.read()
