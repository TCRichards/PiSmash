import subprocess

curDir = '/home/pi/PiSmash/PiCamera/'   # Absolute path to program
# create two files to hold the output and errors, respectively
with open(curDir + 'streamLogs.txt', 'w+') as logs:    # Errors (although everything from streaming is interpreted as an error)
    firstCommand = subprocess.Popen(
        ["""cvlc -vvv v4l2c:///dev/video0:width=640:height=480:chroma=H264 --sout '#rtp{sdp=rtsp://:8554/}' --demux h264"""],
        stderr=logs, shell=True)
    try:
        firstCommand.communicate(timeout=5)  # Executes the command and times out after 5 secs
    except subprocess.TimeoutExpired:   # Kill the first command after 5 secs and launch the second
        firstCommand.kill()
        secondCommand = subprocess.Popen(
            ["""dd if=/dev/video0 bs=1M | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' --demux=h264"""],
            stderr=logs, shell=True)
        secondCommand.communicate()  # Don't force this one to end

    # reset file to read from it
    logs.seek(0)
    # save all stream outputs
    errors = logs.read()
