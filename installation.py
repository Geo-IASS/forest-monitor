import numpy as np
import cableStatics

class InstalledTCS:

    def __init__(self, terrain):
        self.terrain = terrain


    def positionMasts(self, xyPos, height):
        # xyPos is 3 x 2 array with each row being x, y
        self.mastX = [xyPos[i][0] for i in range(3)]
        self.mastY = [xyPos[i][1] for i in range(3)]

        self.mastBaseZ = self.terrain.groundSurface(xyPos)
        self.mastTopZ = self.mastBaseZ + height
        anchorPos = np.zeros((3, 3))
        anchorPos[:, 0:2] = xyPos
        anchorPos[:, 2] = self.mastTopZ

        self.tcs = cableStatics.TriCableSystem(anchorPos, 0.35)


    def positionPlatform(self, xyPos, height, weight):
        z = self.terrain.groundSurface(xyPos) + height
        pb = [xyPos[0], xyPos[1], z]
        self.tcs.setLoad(pb, weight)
        return self.tcs.tune()


    def getTerrainBeneathCables(self, resolution):
        d = range(3)
        zt = range(3)
        zg = range(3)

        for i in range(3):
            numPoints = np.ceil(self.tcs.c[i].w / resolution)
            x = np.linspace(self.tcs.p[i][0], self.tcs.pb[0], numPoints)
            y = np.linspace(self.tcs.p[i][1], self.tcs.pb[1], numPoints)

            d[i] = np.linspace(0, self.tcs.c[i].w, numPoints)

            loc = np.array((x, y)).transpose()

            zt[i] = self.terrain.canopySurface(loc)
            zg[i] = self.terrain.groundSurface(loc)


        return d, zt, zg


    def getCableClearance(self, d, zt):

        zc = range(3)
        minClear = range(3)

        for i in range(3):
            zc[i] = self.tcs.c[i].cableZ(d[i])

            minClear[i] = min(zc[i] - zt[i])


        return zc, min(minClear)



    def platformMap(self, cableRes, gridRes, heightRes, minClearance, maxTension, weight, showProgress=False):
        """Maps the limits of platform height over its entire range.

        Also records cable tension at each location.

        The locations are on an x, y grid.  The interval is given by gridRes.
        The precision of height values at each location is given by heightRes.
        The maximum height is determined by maxTension.  The minimum height at
        each (x, y) locationis determined by maintenance of minClearance between
        the cables and the canopy below.  This is checked along the lengths of
        all cables at a horizontal interval of cableRes along each only.

        This is a slow process.
        """

        def progress(ch):
            '''display characters and flush to stdout immediately'''
            if showProgress:
                import sys
                sys.stdout.write(ch)
                sys.stdout.flush()

        # used to determine is a point is within the mast defined triangle
        import matplotlib.path as mplp

        def roundRange(vals, res):
            '''returns a vector of

            The vector has values uniformly spaced by res.  The range is from
            below the minimum value in vals to just above it.
            '''
            start = np.floor(np.min(vals) / res) * res
            end = np.ceil(np.max(vals) / res) * res
            return np.arange(start, end + res / 2, res)

        # Set the horizontal grid we will map over - it covers the whole range.
        xr = roundRange([self.tcs.p[i][0] for i in range(3)], gridRes)
        yr = roundRange([self.tcs.p[i][1] for i in range(3)], gridRes)

        # establish what is inside the triangle and what's not
        bp = np.array([[self.tcs.p[i][j] for j in range(2)] for i in range(3)])
        bounds = mplp.Path(bp, np.array([1, 2, 2], dtype='uint8'), closed=True)

        # Initialise our readings all to NaN by default

        # tension on each of our cables at each location
        floorTen = np.ones((yr.size, xr.size, 3)) * np.NaN
        ceilTen = np.ones((yr.size, xr.size, 3)) * np.NaN

        zFloor = np.ones((yr.size, xr.size)) * np.NaN
        zCeil = np.ones((yr.size, xr.size)) * np.NaN
        zGround = np.ones((yr.size, xr.size)) * np.NaN

        progress('This could take a while\n\n')
        # Optionally build the x axis for our progress report
        progress('\n{:5} '.format(''))
        for x in xr[6:-1:6]:
            progress('{:>6}'.format(int(x)))
        progress('\n{:5} '.format(''))
        for x in xr[6:-1:6]:
            progress('{:>6}'.format('v'))
        progress('\n')

        for yi in reversed(range(len(yr))):
            y = yr[yi]
            progress('{:5}>'.format(int(y)))
            for xi in range(len(xr)):
                x = xr[xi]
                p = (x,y)

                # for each point ...

                if not bounds.contains_point(p):
                    # We are outside the triangle formed by the three masts,
                    # skip this point.
                    progress('.')
                    continue

                if any([(self.tcs.p[i][0] == x) and (self.tcs.p[i][1] == y) for i in range(3)]):
                    # we are right at a mast.  Skip.
                    progress('#')
                    continue

                # For this point determine the max height (with infinite tension)
                # and the height above the canopy below.
                ceiling = self.tcs.ceiling(p)
                floor = self.terrain.canopySurface(p)

                #TEMP!!! print ceiling, floor
                #TEMP!!! die

                clear = ceiling - floor

                if clear < 0:
                    # The canopy extends up above the ceiling
                    progress('x')
                    continue

                # start finding the maxTension ceiling.
                step = clear * 0.5
                z = floor + step
                self.tcs.setLoad((x, y, z), weight)

                if not self.tcs.tune():
                    # we should really be able to solve the equations for this location ...
                    raise RuntimeError('ceiling error', ceiling, floor, x, y, z)

                while step > heightRes:
                    step *= 0.5
                    ten = self.tcs.tensionAtMasts()
                    if max(ten) > maxTension:
                        z -= step
                    else:
                        lastGoodZ = z
                        lastGoodTen = ten
                        z += step

                    self.tcs.adjustPlatformElevation(z)

                    if not self.tcs.tune():
                        raise RuntimeError('ceiling error', ceiling, floor, x, y, z)

                p3 = (x,y,lastGoodZ)
                self.tcs.setLoad(p3, weight)
                if not self.tcs.tune():
                    raise RuntimeError('ceiling error')

                dist, zt, zg = self.getTerrainBeneathCables(resolution=cableRes)
                zc, mc = self.getCableClearance(d=dist, zt=zt)
                if mc < minClearance:
                    # even at maximum tension we can't ensure clearance of all
                    # cables.
                    progress('_')
                    continue

                zCeil[yi,xi] = lastGoodZ
                ceilTen[yi,xi,:] = lastGoodTen
                zGround[yi,xi] = floor

                clearance = lastGoodZ - floor
                if clearance < 0:
                    raise RuntimeError('ceiling through floor')
                step = clearance * 0.5
                z = floor + step

                while step > heightRes:
                    step *= 0.5
                    #TEMP!!! p3 = (x,y,z)
                    self.tcs.adjustPlatformElevation(z)

                    #TEMP!!! self.tcs.setLoad(p3, weight)
                    if not self.tcs.tune():
                        raise RuntimeError('ceiling error')
                    zc, mc = self.getCableClearance(d=dist, zt=zt)

                    if mc < minClearance:
                        # we need to raise the platform
                        z += step;
                    else:
                        lastGoodZ = z
                        ten = self.tcs.tensionAtMasts()
                        z -= step;

                progress(chr(0x40 + int(z / 20) % 26))
                floorTen[yi,xi, :] = ten
                zFloor[yi,xi] = lastGoodZ
            progress('\n')

        return xr, yr, zCeil, zFloor, zGround, floorTen, ceilTen

