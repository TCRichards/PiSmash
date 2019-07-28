from subprocess import Popen

Popen("""dd if=/dev/video0 bs=1M | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' --demux=h264""", shell=True)
input('Press ENTER to quit')

Popen("""cvlc -vvv v4l2c:///dev/video0:width=640:height=480:chroma=H264 --sout '#rtp{sdp=rtsp://:8554/}' --demux h264""", shell=True)
input('Press ENTER to quit')

Popen("""dd if=/dev/video0 bs=1M | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' --demux=h264""", shell=True)
input('Press ENTER to quit')
