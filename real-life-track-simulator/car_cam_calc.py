import numpy as np
from math import sqrt, tan, atan, radians, degrees
from vector_calc import get_unit, line_plane_collision

# This class handles all car camera calculations
class CarCamCalc:
    CAR_CAM_H = 0.30    # car's camera height from the ground
    CAR_CAM_A = 45      # camera's angle. Zero means pointing downwards
    FRAME_W_2M = 1.0    # frame width in meters at two meters from the camera
    FRAME_H_2M = 1.0    # frame height in meters at two meters from the camera

    down_unit_vec = np.array([0, 0, -1])
    ground_point = np.array([0, 0, 0])
    ground_normal = np.array([0, 0, 1])

    def get_car_cam_coords(self, left_coords, right_coords):
        # get a unit vector from right_coords to left_coords
        rl_vec = -right_coords + left_coords
        rl_unit_vec = rl_vec / np.linalg.norm(rl_vec)
        # get perpendicular vector from it
        perp_rl_unit_vec = np.array([rl_unit_vec[1], -rl_unit_vec[0], 0])
        
        # calculate unitvector to camera pointing direction, and up from camera
        cam_vec = perp_rl_unit_vec + self.down_unit_vec * tan(radians(90 - self.CAR_CAM_A))
        cam_unit_vec = get_unit(cam_vec)
        cam_up_unit_vec = np.cross(cam_unit_vec, rl_unit_vec)

        # calculate car camera coords
        cam_coords = right_coords + rl_vec/2
        cam_coords[2] = self.CAR_CAM_H

        # calculate frame reference vectors
        frame_middle_vec = 2 * cam_unit_vec
        frame_left_middle_vec =  0.5 * self.FRAME_W_2M * rl_unit_vec
        frame_up_middle_vec = 0.5 * self.FRAME_H_2M * cam_up_unit_vec

        # calculate vectors towards frame corner points
        cam_tl_vec = frame_middle_vec + frame_left_middle_vec + frame_up_middle_vec
        cam_bl_vec = frame_middle_vec + frame_left_middle_vec - frame_up_middle_vec
        cam_br_vec = frame_middle_vec - frame_left_middle_vec - frame_up_middle_vec
        cam_tr_vec = frame_middle_vec - frame_left_middle_vec + frame_up_middle_vec

        # get the cornerpoints on the ground
        cam_tl = line_plane_collision(self.ground_normal, self.ground_point, cam_tl_vec, cam_coords)
        cam_bl = line_plane_collision(self.ground_normal, self.ground_point, cam_bl_vec, cam_coords)
        cam_br = line_plane_collision(self.ground_normal, self.ground_point, cam_br_vec, cam_coords)
        cam_tr = line_plane_collision(self.ground_normal, self.ground_point, cam_tr_vec, cam_coords)

        # get points in order so that all of the lines will be drawn. 
        points = np.array([
            cam_coords,
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