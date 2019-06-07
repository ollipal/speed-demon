# Heavily inspired by: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
# Detects red, green and blue circles, draws them to the frame and returns their center coordinates
import imutils
import numpy as np
import cv2


class CircleDetector:
    # define the lower and upper boundaries in the HSV color space
    # more in here: https://stackoverflow.com/questions/17878254/opencv-python-cant-detect-blue-objects
    BLUE_LOWER = np.array([100, 150, 0], np.uint8)
    BLUE_UPPER = np.array([140, 255, 255], np.uint8)

    RED_LOWER = np.array([0, 150, 0], np.uint8)
    RED_UPPER = np.array([10, 255, 255], np.uint8)

    GREEN_LOWER = np.array([24, 70, 120], np.uint8)
    GREEN_UPPER = np.array([60, 255, 255], np.uint8)
    

    def detect_red(self, hsv, frame):
        return self._detect_color(hsv, frame, self.RED_LOWER, self.RED_UPPER, (0, 0, 255))

    def detect_green(self, hsv, frame):
        return self._detect_color(hsv, frame, self.GREEN_LOWER, self.GREEN_UPPER, (0, 255, 0))

    def detect_blue(self, hsv, frame):
        return self._detect_color(hsv, frame, self.BLUE_LOWER, self.BLUE_UPPER, (255, 0, 0))

    def _detect_color(self, hsv, frame, lower_bound, upper_bound, draw_col):
        # construct a mask for the color, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            # TODO make more checks for the radius size before accepting it as correct
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame
                cv2.circle(frame, (int(x), int(y)), int(radius), draw_col, 2)
                cv2.circle(frame, center, 5, draw_col, -1)

        return center
