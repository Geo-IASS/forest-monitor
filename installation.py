import numpy as np
import cableStatics

class InstalledTCS:

    def __init__(self, terrain):
        self.terrain = terrain


    def positionMasts(self, xyPos, height):
        # xyPos is 3 x 2 array with each row being x, y
        self.mastX = [xyPos[i][0] for i in range(3)]
        self.mastY = [xyPos[i][1] for i in range(3)]

        self.mastBaseZ = self.terrain.surface(xyPos)
        self.mastTopZ = self.mastBaseZ + height
        anchorPos = np.zeros((3, 3))
        anchorPos[:, 0:2] = xyPos
        anchorPos[:, 2] = self.mastTopZ

        self.tcs = cableStatics.TriCableSystem(anchorPos, 0.35)


    def positionPlatform(self, xyPos, height, weight):
        z = self.terrain.surface(xyPos) + height
        pb = [xyPos[0], xyPos[1], z]
        self.tcs.setLoad(pb, weight)
        self.tcs.tune()


    def getCableClearance(self):

        d = range(3)
        zc = range(3)
        zg = range(3)

        for i in range(3):
            x = np.linspace(self.tcs.pb[0], self.tcs.p[i][0], 50)
            y = np.linspace(self.tcs.pb[1], self.tcs.p[i][1], 50)

            d[i] = np.linspace(0, self.tcs.c[i].w, 50)
            zc[i] = self.tcs.c[i].cableZ(d[i])

            loc = np.array((x, y)).transpose()

            # print loc

            zg[i] = self.terrain.surface(loc)

        return d, zc, zg





#    def tensionMap(self, resolution, ter, load, thresh):
#
#        import matplotlib.path as mplp
#
#        def roundRange(vals, res):
#            start = np.floor(np.min(vals) / res) * res
#            end = np.ceil(np.max(vals) / res) * res
#            return np.arange(start, end + res / 2, res)
#
#
#        xr = roundRange([tcs.p[i][0] for i in range(3)], resolution)
#        yr = roundRange([tcs.p[i][1] for i in range(3)], resolution)
#
#        bp = np.array([[tcs.p[i][j] for j in range(2)] for i in range(3)])
#        # print(bp)
#        bounds = mplp.Path(bp, np.array([1, 2, 2], dtype='uint8'), closed=True)
#
#        ten = [np.ones((yr.size, xr.size)) * np.NaN for i in range(3)]
#
#        for xi in range(len(xr)):
#            x = xr[xi]
#            for yi in range(len(yr)):
#                y = yr[yi]
#                p = (x,y)
#                if bounds.contains_point(p):
#                    z = ter.surface(p) + 2
#                    tcs.setLoad((x,y,z), load)
#                    tcs.tune()
#                    if max([tcs.c[i].tension()[1] for i in range(3)]) < thresh:
#                        for i in range(3):
#                            ten[i][yi,xi] = tcs.tensionAtMasts()[i]
#
#
#        x,y = np.meshgrid(xr, yr)
#        # print x.shape, y.shape, ten[0].shape
#        ax = plt.subplot(111, projection='3d')
#        ax.plot_wireframe(x, y, ten[0], color='r')
#        ax.plot_wireframe(x, y, ten[1], color='g')
#        ax.plot_wireframe(x, y, ten[2], color='b')
#        plt.xlabel('x')
#        plt.ylabel('y')
#        plt.show()
#
#
