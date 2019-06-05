from offset_calc import OffsetCalc

CAM_H = 1.74    # camera height from the ground
COL_H = 0.2     # color height from the ground


oc = OffsetCalc(500, 250)
print(oc.point_to_offsets([10, 5]))