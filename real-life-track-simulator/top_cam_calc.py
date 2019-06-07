import numpy as np

# Class object will be initialized with picture (or video frame) x- and y-sizes in pixels.
#
# get_col_coords() returns color's coordinates in meters from a point (xy pair in pixels).
# The coordinates are in relation to the origin, that is located CAM_H meters below the camera

class TopCamCalc:
    CAM_H = 1.63        # camera height from the ground
    COL_H = 0.08        # color height from the ground
    FRAME_W_2M = 2.4    # frame width in meters at two meters from the camera


    def __init__(self, pic_size_x, pic_size_y):
        self.pic_size_x = pic_size_x
        self.pic_size_y = pic_size_y
        self.center = [float(pic_size_x)/2.0, float(pic_size_y)/2.0]
        # 0 = center, 100 = the furthest pixel from center
        self.percent_in_pixels = float(max(pic_size_x, pic_size_y))/200.0
        # calculate constant coordinate values
        self.relative_cam_height = self.CAM_H - self.COL_H
        self.relative_cam_coords = np.array([0, 0, self.relative_cam_height])
        self.cam_2m_plane_z = self.relative_cam_height - 2.0

    def get_col_coords(self, point):
        # z-coordinate will be the same as COL_H
        #
        # x- and y-coordinates are calculated by finding the intersection point of xy-plane and line from 
        # relative camera position to 2 meters below the camera with offsets calculated with _point_to_offsets()

        # get the vector from relative camera position towards the offset point 2 meters below
        osp_x, osp_y = self._point_to_offsets(point)
        offset_p = np.array([osp_x, osp_y, self.cam_2m_plane_z])
        vec = offset_p - self.relative_cam_coords

        # get the multiplier t, which tells where the vector intercets the xy-plane (when z=0)
        t = -self.relative_cam_height / vec[2]

        # calculate the intercetion point
        r = self.relative_cam_coords + t*vec

        return r[0], r[1], self.COL_H

    # turns any point (xy pair) from picture to real life offsets [m] at 2 meters from the camera
    def _point_to_offsets(self, point):
        offset_percents = self._get_offset_percents(point)
        return self._offset_percents_to_offset_meters_at_2m(offset_percents)

    def _get_offset_percents(self, point):
        x_offset_perc = (float(point[0]) - self.center[0]) / self.percent_in_pixels
        # pixel counting is reversed compared to "regular" y-axis orientation, the offset in pixels must be multiplied with -1
        y_offset_perc = -(float(point[1]) - self.center[1]) / self.percent_in_pixels
        return [x_offset_perc, y_offset_perc]

    # TODO make more complicated and accurate offset calculations when the actual top camera is available
    def _offset_percents_to_offset_meters_at_2m(self, xy):
        x = (xy[0]/100) * (self.FRAME_W_2M/2.0)
        y = (xy[1]/100) * (self.FRAME_W_2M/2.0)
        return x, y
