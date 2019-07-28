import subprocess

# Popen("""dd if=/dev/video0 bs=1M | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' --demux=h264""", shell=False)
# input('Press ENTER to quit')
#
# Popen("""cvlc -vvv v4l2c:///dev/video0:width=640:height=480:chroma=H264 --sout '#rtp{sdp=rtsp://:8554/}' --demux h264""", shell=False)
# input('Press ENTER to quit')
#
# Popen("""dd if=/dev/video0 bs=1M | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' --demux=h264""", shell=False)
# input('Press ENTER to quit')

# create two files to hold the output and errors, respectively
with open('PiCamera/out.txt', 'w+') as fout:
    with open('PiCamera/err.txt', 'w+') as ferr:
        firstCommand = subprocess.Popen(
            ["""cvlc -vvv v4l2c:///dev/video0:width=640:height=480:chroma=H264 --sout '#rtp{sdp=rtsp://:8554/}' --demux h264"""],
            stdout=fout, stderr=ferr, shell=True)
        try:
            firstCommand.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            firstCommand.kill()
            secondCommand = subprocess.Popen(
                ["""dd if=/dev/video0 bs=1M | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' --demux=h264"""],
                stdout=fout, stderr=ferr, shell=True)
            secondCommand.communicate()  # Don't force this one to end

        # reset file to read from it
        fout.seek(0)
        # save output (if any) in variable
        output = fout.read()

        # reset file to read from it
        ferr.seek(0)
        # save errors (if any) in variable
        errors = ferr.read()
