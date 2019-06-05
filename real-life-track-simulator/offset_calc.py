# class object will be initialized with picture (or video frame) x- and y-sizes in pixels
#
# points_to_offsets() turns any point (xy pair) from picture 
# to real life offsets [m] at 2 meters from the camera

class OffsetCalc:
    def __init__(self, pic_size_x, pic_size_y):
        self.center = [float(pic_size_x)/2, float(pic_size_y)/2]
        # 0 = center, 100 = the furthest pixel from center
        percent_in_pixels = float(max(pic_size_x, pic_size_y))/200
        self.pixel_offset_in_perc = lambda pixel_offset: pixel_offset / percent_in_pixels

    def point_to_offsets(self, point):
        offset_percents = self._get_offset_percents(point)
        return self._offset_percents_to_offset_meters_at_2m(offset_percents)

    def _get_offset_percents(self, point):
        x_offset_perc = self.pixel_offset_in_perc(point[0] - self.center[0])
        # pixel counting is reversed compared to "regular" y-axis orientation, the offset in pixels must be multiplied with -1
        y_offset_perc = self.pixel_offset_in_perc(-1 * (point[1] - self.center[1]))
        return [x_offset_perc, y_offset_perc]

    # TODO make more complicated and accurate offset calculations with the Pi Camera
    def _offset_percents_to_offset_meters_at_2m(self, xy):
        real_life_width = 1.97
        x = (xy[0]/100) * (real_life_width/2)
        y = (xy[1]/100) * (real_life_width/2)
        return [x, y]
