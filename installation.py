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
        return self.tcs.tune()


    def getCableClearance(self, resolution):

        d = range(3)
        zc = range(3)
        zg = range(3)
        minClear = range(3)

        for i in range(3):
            numPoints = np.ceil(self.tcs.c[i].w / resolution)
            x = np.linspace(self.tcs.p[i][0], self.tcs.pb[0], numPoints)
            y = np.linspace(self.tcs.p[i][1], self.tcs.pb[1], numPoints)

            d[i] = np.linspace(0, self.tcs.c[i].w, numPoints)
            zc[i] = self.tcs.c[i].cableZ(d[i])

            loc = np.array((x, y)).transpose()

            # print loc

            zg[i] = self.terrain.surface(loc)

            minClear[i] = min(zc[i] - zg[i])

        return d, zc, zg, min(minClear)





    def tensionMap(self, cableRes, gridRes, minClearance, maxTension, weight):

        import matplotlib.path as mplp

        def roundRange(vals, res):
            start = np.floor(np.min(vals) / res) * res
            end = np.ceil(np.max(vals) / res) * res
            return np.arange(start, end + res / 2, res)

        xr = roundRange([self.tcs.p[i][0] for i in range(3)], gridRes)
        yr = roundRange([self.tcs.p[i][1] for i in range(3)], gridRes)

        bp = np.array([[self.tcs.p[i][j] for j in range(2)] for i in range(3)])
        bounds = mplp.Path(bp, np.array([1, 2, 2], dtype='uint8'), closed=True)

        maxTen = np.ones((yr.size, xr.size)) * np.NaN
        height = np.ones((yr.size, xr.size)) * np.NaN
        # z = np.ones((yr.size, xr.size)) * np.NaN

        for xi in range(len(xr)):
            x = xr[xi]
            for yi in range(len(yr)):
                y = yr[yi]
                p = (x,y)

                if bounds.contains_point(p):
                    print 'point', p,

                    h = 0
                    cont = True
                    while cont:
                        if self.positionPlatform([x, y], h, weight):
                            d, zc, zg, mc = self.getCableClearance(resolution=cableRes)
                            if mc < minClearance:
                                h += 2
                                print '.',
                            else:
                                ten = max(self.tcs.tensionAtMasts())
                                if ten < maxTension:
                                    maxTen[yi,xi] = ten
                                    height[yi,xi] = h
                                    print h, ten
                                else:
                                    print 'overtension'
                                cont = False
                        else:
                            print 'too high'
                            cont = False
        return xr, yr, maxTen, height


