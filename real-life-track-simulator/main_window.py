import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from matplotlib._png import read_png
from car_cam_calc import CarCamCalc


class MainWindow:
    def __init__(self, tcc, show_road=False):
        # tcc means TopCamCalc
        self.tcc = tcc
        self.ccc = CarCamCalc()
        # get left top corner coordinates
        corner_coords = tcc.get_col_coords([0, 0])

        # allow plot data updates
        plt.ion()

        # setup 3D plot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        # force equal scaling, 
        # more here: https://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to
        max_range = max(tcc.CAM_H/2, corner_coords[0], corner_coords[1])
        self.ax.set_xlim(-max_range, max_range)
        self.ax.set_ylim(-max_range, max_range)
        self.ax.set_zlim(tcc.CAM_H/2 - max_range, tcc.CAM_H/2 + max_range)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # setup road
        # due to a bad performance, the default is just use blue surface as road
        if show_road:
            img = read_png("road.png")
            road_res = 50
            x, y = np.meshgrid(np.linspace(-corner_coords[0], corner_coords[0], num=road_res), np.linspace(-corner_coords[1], corner_coords[1], num=road_res))
            z = np.zeros((len(x), 1))
            self.ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=img, alpha=0.99)
        else:
            x, y = np.meshgrid(np.linspace(-corner_coords[0], corner_coords[0], num=2), np.linspace(-corner_coords[1], corner_coords[1], num=2))
            z = np.zeros((len(x), 1))
            self.ax.plot_surface(x, y, z, facecolor="blue", alpha=0.2)

        # show empty plot
        plt.draw()
        plt.pause(0.5)

        # setup color points
        self.reds = None
        self.greens = None
        self.blues = None
        # set up magentas (car cam)
        self.magentas = None

    def plot_red(self, point):
        if self.reds is not None:
            self.reds.remove()
            self.reds = None
        return self._plot_color(point, "r")
    
    def plot_green(self, point):
        if self.greens is not None:
            self.greens.remove()
            self.greens = None
        return self._plot_color(point, "g")

    def plot_blue(self, point):
        if self.blues is not None:
            self.blues.remove()
            self.blues = None
        return self._plot_color(point, "b")

    def _plot_color(self, point, col):
        x = y = z = None
        if point is not None:
            x, y, z = self.tcc.get_col_coords(point)
            self._scatter_point(x, y, z, col)
        
        return np.array([x, y, z])

    def _scatter_point(self, x, y, z, col):
        pts = self.ax.scatter(x, y, z, c=col)
        if col == "r":
            self.reds = pts
        elif col == "g":
            self.greens = pts
        elif col == "b":
            self.blues = pts

        plt.draw()
        #plt.pause(0.5) #very useful when debugging


    def plot_car_cam(self, left_coords, right_coords):
        if left_coords[0] is not None and right_coords[0] is not None:
            x, y, z = self.ccc.get_car_cam_coords(left_coords, right_coords)
            if self.magentas is not None:
                self.magentas.pop(0).remove()
                self.magentas = None
            self.magentas = self.ax.plot(x, y, z, c="m")
            plt.draw()

