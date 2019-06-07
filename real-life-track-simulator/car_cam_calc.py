import numpy as np
from math import sqrt, tan, radians

# This class handles all car camera calculations
class CarCamCalc:
    CAR_CAM_H = 0.30    # car's camera height from the groun
    CAR_CAM_A = 55      # camera's angle. Zero means pointing downwards
    FRAME_W_2M = 1.0    # frame width in meters at two meters from the camera
    FRAME_H_2M = 0.7    # frame height in meters at two meters from the camera


    def __init__(self):
        self.down_unit_vec = np.array([0, 0, -1])

    def get_car_cam_coords(self, left_coords, right_coords):
        # get vector from left_coords to right_coords
        rl_vec = -right_coords + left_coords

        # get unit vector from rl_vec, and perpendicular vector from it
        rl_unit_vec = rl_vec / np.linalg.norm(rl_vec)
        perp_rl_unit_vec = np.array([rl_unit_vec[1], -rl_unit_vec[0], 0])
        
        # calculate unitvector to camera pointing direction, and up from camera
        cam_vec = perp_rl_unit_vec + self.down_unit_vec * tan(radians(90 - self.CAR_CAM_A))
        cam_unit_vec = cam_vec / np.linalg.norm(cam_vec)
        # pythagoras:
        xy_len = sqrt(cam_unit_vec[0]**2 + cam_unit_vec[1]**2)
        xy_mult = cam_unit_vec[2] / xy_len
        cam_up_unit_vec = np.array([xy_mult*cam_unit_vec[0], xy_mult*cam_unit_vec[1], -xy_len])

        # calculate car camera coords
        cam_coords = right_coords + rl_vec/2
        cam_coords[2] = self.CAR_CAM_H

        # calculate frame reference points
        frame_middle_coords = cam_coords + 2*cam_unit_vec
        frame_top_middle_coords = frame_middle_coords + 0.5 * self.FRAME_H_2M * cam_up_unit_vec

        # calculate frame corner points at 2 meters from camera
        cam_tl_2m = frame_top_middle_coords + 0.5 * self.FRAME_W_2M * rl_unit_vec
        cam_bl_2m = cam_tl_2m - self.FRAME_H_2M * cam_up_unit_vec
        cam_br_2m = cam_bl_2m - self.FRAME_W_2M * rl_unit_vec
        cam_tr_2m = cam_br_2m + self.FRAME_H_2M * cam_up_unit_vec

        # get t multipliers, which will help the point in which the points touch the ground
        t_tl = -self.CAR_CAM_H / cam_tl_2m[2]
        t_bl = -self.CAR_CAM_H / cam_bl_2m[2]
        t_br = -self.CAR_CAM_H / cam_br_2m[2]
        t_tr = -self.CAR_CAM_H / cam_tr_2m[2]

        # get the cornerpoints on the ground
        cam_tl = cam_coords + t_tl * (-cam_coords + cam_tl_2m)
        cam_bl = cam_coords + t_bl * (-cam_coords + cam_bl_2m)
        cam_br = cam_coords + t_br * (-cam_coords + cam_br_2m)
        cam_tr = cam_coords + t_tr * (-cam_coords + cam_tr_2m)

        # TODO fix calculation so there would not be a need for this
        # currently, for some reason z-values are slightly below 0 after calculations 
        cam_tl[2] = 0
        cam_bl[2] = 0
        cam_br[2] = 0
        cam_tr[2] = 0

        # get points in order so that all of the lines will be drawn. 
        points = np.array([
            cam_tl,
            cam_bl,
            cam_coords,
            cam_tl,
            cam_tr,
            cam_coords,
            cam_br,
            cam_tr,
            cam_br,
            cam_bl
        ])

        # separate xs, ys and zs for returning and plotting
        return points.T