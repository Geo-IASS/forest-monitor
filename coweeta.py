import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import osgeo.ogr as oo

import scipy.ndimage

import gdal

import cableStatics

class Coweeta:
    def __init__(self):
        self.g = gdal.Open('cwt_dem/w001001.adf')

        a = self.g.ReadAsArray()
        self.zg = np.array(a, dtype=float)
        self.zg[a == -32768] = np.NaN
        self.zg = self.zg.transpose()
        self.zg0 = self.zg.copy()
        self.zg0[np.isnan(self.zg0)] = 0

        self.gt = self.g.GetGeoTransform()
        self.step = np.array([self.gt[1], self.gt[5]])
        self.origin = np.array([self.gt[0], self.gt[3]])

        #self.xg = self.xStep * np.arange(0, g.RasterXSize)
        #self.yg = self.yStep * np.arange(0, g.RasterYSize)


    def setOrigin(self, loc):
        self.refPoint = loc
        self.origin = np.array([self.gt[0] - loc[0], self.gt[3] - loc[1]])


    def xValues(self, gis):
        return [point[0] - self.refPoint[0] for point in gis]


    def yValues(self, gis):
        return [point[1] - self.refPoint[1] for point in gis]


    def locationToIndices(self, loc):
        # Scales the given (x,y) coordinates to correspond with the indexing of
        # the DEM array.
        return (loc - self.origin) / self.step


    def range(self):
        # Returns two (x,y) points, one at either corner of the basin data.
        return self.origin, self.origin + self.step * self.zg.shape


    def map(self, p1, p2, ax=None):
        # display a contour map of the basin bounded by the rectangle defined by
        # (x,y) points p1 and p2.
        doAll = not(ax)
        if doAll:
            ax = plt.subplot(111, aspect='equal')
        plt.xlabel('metres E-W')
        plt.ylabel('metres N-S')
        p1i, p2i = self.locationToIndices(p1), self.locationToIndices(p2)
        p1i, p2i = np.min([p1i, p2i], axis=0), np.max([p1i, p2i], axis=0)
        p1i = np.array(np.floor(np.max([p1i, (0, 0)],        axis=0)), dtype=int)
        p2i = np.array(np.ceil( np.min([p2i, self.zg.shape], axis=0)), dtype=int)
        print p1i
        print p2i
        xi, yi = [np.arange(p1i[a], p2i[a]) for a in [0, 1]]
        xr, yr = [np.arange(p1i[a], p2i[a]) * self.step[a] + self.origin[a] for a in [0, 1]]
        x, y = np.meshgrid(xr, yr)
        z = self.zg[xi, np.reshape(yi, (len(yi), 1))]
        ax.contour(x, y, z, 20, cmap=cm.coolwarm)
        return ax


    def combPlot(self, p1, p2, ax):
        doAll = not(ax)
        if doAll:
            ax = plt.subplot(111, projection='3d') # , aspect='equal')
        plt.xlabel('metres E-W')
        plt.ylabel('metres N-S')
        p1i, p2i = self.locationToIndices(p1), self.locationToIndices(p2)
        # print 'a', p1i, p2i
        p1i, p2i = np.min([p1i, p2i], axis=0), np.max([p1i, p2i], axis=0)
        # print 'b', p1i, p2i
        p1i = np.array(np.floor(np.max([p1i, (0, 0)],        axis=0)), dtype=int)
        p2i = np.array(np.ceil( np.min([p2i, self.zg.shape], axis=0)), dtype=int)
        # print 'c', p1i, p2i
        xi, yi = [np.arange(p1i[a], p2i[a]) for a in [0, 1]]
        # print p1i
        # print p2i
        # print max(xi), xi.shape, max(yi), yi.shape
        xr, yr = [np.arange(p1i[a], p2i[a]) * self.step[a] + self.origin[a] for a in [0, 1]]
        # print xr.shape, yr.shape

        x, y = np.meshgrid(xr, yr)
        # print x.shape, y.shape
        z = self.zg[xi, np.reshape(yi, (len(yi), 1))]

        # print z.shape

        ax.contour(x, y, z, 20, cmap=cm.coolwarm)
        # ax.contour(x, y, z, 20, zdir='z', offset=0, cmap=cm.coolwarm)

        # ax.plot_wireframe(x, y, z, rstride=20, cstride=20)

        ax.plot_surface(x, y, z, rstride=20, cstride=20, alpha=0.3, linewidth=0)

        return ax


    def surface(self, loc):
        locI = self.locationToIndices(loc)
        #x = locI[:,0]
        #y = locI[:,1]
        if locI.shape == (2,):
            z = scipy.ndimage.map_coordinates(self.zg0, locI.reshape(2,1))
        else:
            z = scipy.ndimage.map_coordinates(self.zg0, locI.transpose())
        return z


def new3d():
    ax = plt.subplot(111, projection='3d') # , aspect='equal')
    plt.xlabel('metres E-W')
    plt.ylabel('metres N-S')
    return ax


def doStream():
    # import coweeta
    # reload(-coweeta)
    c = Coweeta()

    s = oo.Open('coweeta_streams/coweeta_streams.dbf')
    l = s.GetLayerByIndex(0)
    numFeat = l.GetFeatureCount()
    ax = new3d()
    c.combPlot([0,0], [1e7,1e7], ax)
    for i in range(numFeat):
        f = l.GetFeature(i)
        gr = f.GetGeometryRef()
        p = np.array(gr.GetPoints())
        #print p.shape,
        #print np.min(p), np.max(p)
        z = c.surface(p)
        x = p[:,0]
        y = p[:,1]
        #print x.shape, y.shape, z.shape
        #print y
        #print z
        #print
        ax.plot(x, y, z,'r')

    plt.show()


def doWire():
    c = Coweeta()
    c.setOrigin((275000, 3880000))
    ax = new3d()
    #TEMP!!! ax = plt.subplot(111)
    #TEMP!!! ax.contour(x,y,z)
    c.combPlot([0,0], [1e7,1e7], ax)
    plt.show()

import presentation

class InstalledTCS:

    def __init__(self, c):
        self.c = c


    def positionTowers(self, xyPos, height):
        # xyPos is 3 x 2 array with each row being x, y
        self.towerX = [xyPos[i][0] for i in range(3)]
        self.towerY = [xyPos[i][1] for i in range(3)]

        self.towerBaseZ = self.c.surface(xyPos)
        self.towerTopZ = self.towerBaseZ + height
        anchorPos = np.zeros((3, 3))
        anchorPos[:, 0:2] = xyPos
        anchorPos[:, 2] = self.towerTopZ

        self.tcs = cableStatics.TriCableSystem(anchorPos, 0.35)


    def positionPlatform(self, xyPos, height, weight):
        z = self.c.surface(xyPos) + height
        pb = [xyPos[0], xyPos[1], z]
        self.tcs.setLoad(pb, weight)
        self.tcs.tune()


    def report(self, nw, se):
        ax = ax = plt.subplot(111, projection='3d')
        self.c.combPlot(nw, se, ax)

        for i in range(3):
            presentation.tower(self.towerX[i], self.towerY[i], self.towerBaseZ[i], self.towerTopZ[i], ax)

            x = np.linspace(self.tcs.pb[0], self.towerX[i], 50)
            y = np.linspace(self.tcs.pb[1], self.towerY[i], 50)
            d = np.linspace(0, self.tcs.c[i].w, 50)
            zc = self.tcs.c[i].cableZ(d)
            zg = self.c.surface(np.transpose([x,y]))

            ax.plot(x, y, zc, 'b')
            ax.plot(x, y, zg, 'g')

            text = 'T = {0:0.0f}N\nL = {1:0.0f}m'.format(self.tcs.c[i].tension()[1], self.tcs.c[i].length()[0])
            #TEMP!!! print text  #TEMP!!!
            ax.text(self.towerX[i], self.towerY[i], self.towerTopZ[i], text)



        ax.plot([self.tcs.pb[0]], [self.tcs.pb[1]], [self.tcs.pb[2]], 'ro')

        return ax



def doAll():
    c = Coweeta()
    c.setOrigin((275000,3880000))

    xt = [2330,2586,2310]
    yt = [845,913,1090]
    np.array([xt,yt])
    np.array([xt,yt]).transpose()
    ztb = c.surface(np.array([xt,yt]).transpose())
    ztt = ztb + 30

    pa = [np.array([xt[i],yt[i],ztt[i]]) for i in range(3)]
    pb = np.array([2400,950,800])
    tcs = cableStatics.TriCableSystem(pa, 0.35)
    tcs.setLoad(pb, 10)
    tcs.tune()

    cableStatics.tensionMap(tcs, 5, c, 100, 200)

    c.combPlot((2200,800),(2600,1100))
    # cableStatics.report(tcs)

    for i in range(3):
        cableStatics.tower(xt[i], yt[i], ztb[i], ztt[i])

        x = np.linspace(tcs.pb[0], tcs.p[i][0], 50)
        y = np.linspace(tcs.pb[1], tcs.p[i][1], 50)
        d = np.linspace(0, tcs.c[i].w, 50)
        zc = tcs.c[i].cableZ(d)
        zg = c.surface(np.transpose([x,y]))
        # plt.plot([tcs.pb[0], tcs.p[i][0]], [tcs.pb[1], tcs.p[i][1]], [0, 0], 'g')
        # tower(tcs.p[i][0], tcs.p[i][1], 0, tcs.p[i][2])
        plt.plot(x, y, zc, 'b')
        plt.plot(x, y, zg, 'g')

    plt.plot([tcs.pb[0]], [tcs.pb[1]], [tcs.pb[2]], 'ro')


    plt.show()


#
# import numpy as np
# import matplotlib.pyplot as plt
# import osgeo.ogr as oo
# s = oo.Open('coweeta_streams/coweeta_streams.dbf')
# l = s.GetLayerByIndex(0)
# numFeat = l.GetFeatureCount()
# plt.figure()
# for i in range(numFeat):
#     f = l.GetFeature(i)
#     gr = f.GetGeometryRef()
#     p = np.array(gr.GetPoints())
#     px = p[:,0]
#     py = p[:,1]
#     ax.plot(px, py, z)
#
# plt.show()
#
#
#
#
#
#
# def getMeshgrid(g):
#     return np.meshgrid(xr, yr)
#
# def getMeshgridNoOffset(g):
#     gt = g.GetGeoTransform()
#     xr = np.arange(0, gt[1] * (g.RasterXSize - 0.5), gt[1])
#     yr = np.arange(0, gt[5] * (g.RasterYSize - 0.5), gt[5])
#     return np.meshgrid(xr, yr)
#
# def zoomArea(xf, yf, zf, xr, yr):
#     xm = np.nonzero((xf[0,:] >= xr[0]) & (xf[0,:] <= xr[1]))[0]
#     ym = np.nonzero((yf[:,0] >= yr[0]) & (yf[:,0] <= yr[1]))[0]
#     ym = ym.reshape((ym.size, 1))
#     return xf[xm, ym], yf[xm, ym], zf[xm, ym]
#
#
# def plotTransect(x, y, z, xi, yi):
#     axx = plt.subplot(211)
#     axy = plt.subplot(212)
#
#     axx.plot(x[0,:], z[yi,:])
#     axx.plot(x[0,xi], z[yi,xi], 'ro')
#     axx.set_ylim([600,1400])
#     axx.set_xlabel('EW [m]')
#
#     axy.plot(y[:,0], z[:,xi])
#     axy.plot(y[yi,0], z[yi,xi], 'ro')
#     axy.set_ylim([600,1400])
#     axy.set_xlabel('NS [m]')
#
#     plt.show()
#
# def xy2pixel(x, y, xm, ym):
#     pass
#

# # from http://stackoverflow.com/questions/7878398/how-to-extract-an-arbitrary-line-of-values-from-a-numpy-array
#
# import numpy as np
# import scipy.ndimage
# import matplotlib.pyplot as plt
#
# #-- Generate some data...
# x, y = np.mgrid[-5:5:0.1, -5:5:0.1]
# z = np.sqrt(x**2 + y**2) + np.sin(x**2 + y**2)
#
# #-- Extract the line...
# # Make a line with "num" points...
# x0, y0 = 5, 4.5 # These are in _pixel_ coordinates!!
# x1, y1 = 60, 75
# num = 1000
# x, y = np.linspace(x0, x1, num), np.linspace(y0, y1, num)
#
# # Extract the values along the line, using cubic interpolation
# zi = scipy.ndimage.map_coordinates(z, np.vstack((x,y)))
#
# #-- Plot...
# fig, axes = plt.subplots(nrows=2)
# axes[0].imshow(z)
# axes[0].plot([x0, x1], [y0, y1], 'ro-')
# axes[0].axis('image')
#
# axes[1].plot(zi)
#
# plt.show()
