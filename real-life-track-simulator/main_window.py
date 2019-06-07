import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class MainWindow:
    def __init__(self, tcc):
        # tcc = TopCamCalc
        self.tcc = tcc
        # get left top corner coordinates
        corner_coords = tcc.get_col_coords([0, 0])

        # allow plot data updates
        plt.ion()

        # setup 3D plot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        # set x- and y-limits according to camera
        self.ax.set_xlim3d(corner_coords[0], -corner_coords[0])
        self.ax.set_ylim3d(-corner_coords[1], corner_coords[1])
        self.ax.set_zlim3d(0, self.tcc.CAM_H)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        # TODO self.ax.axis('equal') can this be done in 3d?

        # show empty plot
        plt.draw()
        plt.pause(0.5)

        # setup color points
        self.reds = None
        self.greens = None
        self.blues = None

    def plot_red(self, point):
        if self.reds is not None:
            self.reds.remove()
            self.reds = None
        self._plot_color(point, "r")
    
    def plot_green(self, point):
        if self.greens is not None:
            self.greens.remove()
            self.greens = None
        self._plot_color(point, "g")

    def plot_blue(self, point):
        if self.blues is not None:
            self.blues.remove()
            self.blues = None
        self._plot_color(point, "b")

    def _plot_color(self, point, col):
        if point is not None:
            x, y, z = self.tcc.get_col_coords(point)
            pts = self.ax.scatter(x, y, z, c=col)
            if col == "r":
                self.reds = pts
            elif col == "g":
                self.greens = pts
            else: # "b"
                self.blues = pts

            plt.draw()
            #plt.pause(1) pauses are very useful when debugging
