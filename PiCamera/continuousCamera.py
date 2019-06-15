import time
from picamera import PiCamera
from picamera.array import PiRGBArray       # PiRGBArray is an object that wraps a 3D numpy array
import cv2
import numpy as np

                              
# Setup code############
# Our ouput array is of size 3*width*height*MAX, so we are forded to use lower resolution
im_width, im_height = 688, 400          # Image resolution
MAX = 100                               # Maximum number of images allowed. True count may be smaller if time is exceeded
imageCount = MAX                        # If we don't use all the array space, this is the true size

camera = PiCamera()
camera.resolution = (im_width, im_height)
rawCapture = PiRGBArray(camera, size = (im_width, im_height))   # Immediate storage location for capture_continuous
rawCapture.truncate(0)
outputs = np.zeros((MAX, im_height, im_width, 3), dtype = float) # 3 color channels, each of width im_width and height im_height, for each of MAX images
# For some reason, needed to swap im_width with im_height from rawCapture -> outputs for sizing to work
#########################

def capture_images(secs):
    global camera, rawCapture, outputs
    camera.start_preview() # Open the camera
    time.sleep(2)               # Give delay for camera to adjust
    endTime = time.time() + secs
    
    try:
        # Iterates image by image through a continuous stream. Each image is stored in the next index of outputs
        for i, frame1 in enumerate(camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True)): 
            
            frame = np.copy(frame1.array)
            frame.setflags(write=1)
            outputs[i, :, :, :] = np.copy(frame)/255 # Normalize the RGB values to 0-1
            rawCapture.truncate(0)                   # Clear the raw capture object for reuse

            if cv2.waitKey(1) == ord('q') or i >= MAX-1 or time.time() >= endTime:
                return
    except:
        print("ERROR")
    finally:  # This block is executed even if returns above
        camera.stop_preview()
        camera.close()
        cv2.destroyAllWindows()
        return

def main():
    global camera, rawCapture, outputs

    
    capture_images(2)
    cv2.imwrite('outputTest.jpg', outputs[0])    # Save the first image in the directory
    cv2.imshow('First Output Image', outputs[0]) # Display the first image 
    while (cv2.waitKey(1) != ord('q')):          # Exit application by pressing 'q'
        continue
    cv2.destroyAllWindows()
    
main()
    