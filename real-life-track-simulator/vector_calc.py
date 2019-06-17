import numpy as np

# Line-plane intersection
# By Tim Sheerman-Chase
# This software may be reused under the CC0 license
# https://gist.github.com/TimSC/8c25ca941d614bf48ebba6b473747d72
def line_plane_collision(planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-6):
    ndotu = planeNormal.dot(rayDirection)
    if abs(ndotu) < epsilon:
	    raise RuntimeError("no intersection or line is within plane")

    w = rayPoint - planePoint
    si = -planeNormal.dot(w) / ndotu
    Psi = w + si * rayDirection + planePoint
    return Psi

def get_unit(vec):
    return vec / np.linalg.norm(vec)