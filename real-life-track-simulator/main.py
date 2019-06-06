'''
This is the main loop in the simulator. 
It defaults to onboard camera but a video file name can be supplied too wtih --video or -v.
The loop can be terminated by pressing 'q' on the keyboard

If Anaconda is used, the dependensies can be installed to an separate environment with following commands:
    conda create -n [NAME] python=3.6 numpy matplotlib pip
    conda activate [NAME]
    pip install imutils opencv-python
'''

from imutils.video import VideoStream
import imutils
import cv2
import time
import argparse
from circle_detector import CircleDetector


def main(video_file_name=None):
    if video_file_name is None:
        vs = VideoStream(src=0).start()
        time.sleep(1) # allow the camera to warm up
    else:
	    vs = cv2.VideoCapture(video_file_name)
    
    # initialize the CircleDetector
    cd = CircleDetector()

    # start the main loop
    while True:
        # grab the current frame
        frame = vs.read()
        # handle the frame from VideoCapture or VideoStream
        if video_file_name is not None:
            frame = frame[1]
        
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if frame is None:
            break
        
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        red_center = cd.detect_red(hsv, frame)
        green_center = cd.detect_green(hsv, frame)
        blue_center = cd.detect_blue(hsv, frame)
        
        # show the frame to our screen
        # TODO make showing the picture optional
        cv2.imshow("Frame", frame)
        
        # if the 'q' key is pressed, stop the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
 
    # stop the camera video stream or release the camera
    if video_file_name is None:
        vs.stop()
    else:
        vs.release()

    # close all windows
    cv2.destroyAllWindows()

# get argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
args = vars(ap.parse_args())

# check if video file name was supplied
# if not then try to use the onboard camera stream 
main(video_file_name=args.get("video", None))
