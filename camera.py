import sys
sys.path.append("/usr/local/lib")
import time
import pyrealsense2 as rs
import numpy as np
import cv2
from myconfig import IMAGE_W, IMAGE_H
from donkeycar.parts.camera import BaseCamera


class RealSenseCamera(BaseCamera):
    def __init__(self, resolution=(848, 800), framerate=20): 
        cfg = rs.config()
        self.pipeline = rs.pipeline()

        cfg.enable_stream(rs.stream.fisheye, 1) # Left camera
        cfg.enable_stream(rs.stream.fisheye, 2) # Right camera

        self.pipeline.start(cfg)
        self.frame = None
        self.on = True

        print('RealSense Camera loaded... warming up camera')
        time.sleep(2)

    def run(self):
        frames = self.pipeline.wait_for_frames()
        
        left = np.asanyarray(frames.get_fisheye_frame(1).get_data())
        right = np.asanyarray(frames.get_fisheye_frame(2).get_data())

        left = left[352:592, 21:831]
        right = right[352:592, 21:831]
        
        frame = np.concatenate((left, right), axis=0)
        #frame = cv2.resize(frame, (230, 180))
        #frame = cv2.resize(frame, (160, 120))
        frame = cv2.resize(frame, (IMAGE_W, IMAGE_H))
        frame = cv2.blur(frame, (2, 2))
        ret, frame = cv2.threshold(frame, 210, 255, cv2.THRESH_BINARY)

        frame = np.expand_dims(frame, -1)
        return frame
        '''
        left = frames.get_fisheye_frame(1)
        right = frames.get_fisheye_frame(2)
        left_frame = np.asanyarray(left.get_data())
        cv2.putText(left_frame, 'Dist', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2, cv2.LINE_AA)
        
        #left_frame = cv2.cvtColor(left_frame,cv2.COLOR_GRAY2BGR)

       # right_frame = np.asanyarray(right.get_data())
        left_frame_small = cv2.resize(left_frame, (160, 120))
        left_frame_small = np.expand_dims(left_frame_small, -1)
        
        #frame = left_frame
        #ret, frame = cv2.threshold(frame, 200, 255, cv2.THRESH_BINARY)
        #frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
        #frame[np.where((frame==[255,255,255]).all(axis=2))] = [0,0,255]
        #frame[np.where((frame==[0,0,0]).all(axis=2))] = [255,0,0]
        return left_frame_small
        right_frame_small = cv2.resize(right_frame, (160, 120))
        stereo_frame = np.concatenate((left_frame_small, right_frame_small), axis=1)
        stereo_frame = cv2.putText(stereo_frame, 'Dist', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2, cv2.LINE_AA)
        return stereo_frame
        #return self.blank_image
        '''

    def update(self):
        while True:
            self.frame = self.run()

            if not self.on:
                break


    def shutdown(self):
        self.on = False
        print('Stopping RealSense Camera')
        self.pipeline.stop()
