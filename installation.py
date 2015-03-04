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



    def platformMap(self, cableRes, gridRes, heightRes, minClearance, maxTension, weight):

        def prog(ch):
            import sys
            sys.stdout.write(ch)
            sys.stdout.flush()

        import matplotlib.path as mplp

        def roundRange(vals, res):
            start = np.floor(np.min(vals) / res) * res
            end = np.ceil(np.max(vals) / res) * res
            return np.arange(start, end + res / 2, res)

        xr = roundRange([self.tcs.p[i][0] for i in range(3)], gridRes)
        yr = roundRange([self.tcs.p[i][1] for i in range(3)], gridRes)

        bp = np.array([[self.tcs.p[i][j] for j in range(2)] for i in range(3)])
        bounds = mplp.Path(bp, np.array([1, 2, 2], dtype='uint8'), closed=True)

        floorTen = np.ones((yr.size, xr.size)) * np.NaN
        zFloor = np.ones((yr.size, xr.size)) * np.NaN
        zCeil = np.ones((yr.size, xr.size)) * np.NaN
        zGround = np.ones((yr.size, xr.size)) * np.NaN

        for yi in range(len(yr)):
            y = yr[yi]
            prog('>')
            for xi in range(len(xr)):
                x = xr[xi]
                p = (x,y)

                if not bounds.contains_point(p):
                    prog('.')

                    continue

                ceiling = self.tcs.ceiling(p)
                floor = self.terrain.surface(p)

                dist = ceiling - floor

                if dist < 0:
                    prog('x')

                    continue
                step = dist * 0.5
                z = floor + step

                while step > heightRes:
                    step *= 0.5
                    p3 = (x,y,z)
                    self.tcs.setLoad(p3, weight)

                    if not self.tcs.tune():
                        raise RuntimeError('ceiling error')
                    ten = max(self.tcs.tensionAtMasts())
                    if ten > maxTension:
                        z -= step
                    else:
                        lastGoodZ = z
                        z += step
                p3 = (x,y,lastGoodZ)
                self.tcs.setLoad(p3, weight)
                if not self.tcs.tune():
                    raise RuntimeError('ceiling error')
                d, zc, zg, mc = self.getCableClearance(resolution=cableRes)
                if mc < minClearance:
                    prog('_') # print '_', # mc < minClearance'
                    continue

                zCeil[yi,xi] = lastGoodZ
                zGround[yi,xi] = floor

                dist = lastGoodZ - floor
                if dist < 0:
                    raise RuntimeError('ceiling through floor')
                step = dist * 0.5
                z = floor + step

                while step > heightRes:
                    step *= 0.5
                    p3 = (x,y,z)
                    self.tcs.setLoad(p3, weight)
                    if not self.tcs.tune():
                        raise RuntimeError('ceiling error')
                    d, zc, zg, mc = self.getCableClearance(resolution=cableRes)

                    if mc < minClearance:
                        z += step;
                    else:
                        lastGoodZ = z
                        ten = max(self.tcs.tensionAtMasts())
                        z -= step;

                prog(chr(0x40 + int(z / 20) % 26))
                floorTen[yi,xi] = ten
                zFloor[yi,xi] = lastGoodZ
            prog('<\n')


        return xr, yr, zCeil, zFloor, zGround, floorTen

