import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import osgeo.ogr as oo
import scipy.ndimage

import gdal
import json



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


    def setWorkingRefPoint(self, loc):
        # Set a local reference point.
        self.refPoint = loc
        self.origin = np.array([self.gt[0] - loc[0], self.gt[3] - loc[1]])


    def surfaceMesh(self, p1, p2):

        p1i, p2i = self.locationToIndices(p1), self.locationToIndices(p2)

        p1i, p2i = np.min([p1i, p2i], axis=0), np.max([p1i, p2i], axis=0)

        p1i = np.array(np.floor(np.max([p1i, (0, 0)],        axis=0)), dtype=int)
        p2i = np.array(np.ceil( np.min([p2i, self.zg.shape], axis=0)), dtype=int)

        xi, yi = [np.arange(p1i[a], p2i[a]) for a in [0, 1]]
        xr, yr = [np.arange(p1i[a], p2i[a]) * self.step[a] + self.origin[a] for a in [0, 1]]

        x, y = np.meshgrid(xr, yr)
        z = self.zg[xi, np.reshape(yi, (len(yi), 1))]

        return x, y, z


    def locationToIndices(self, loc):
        # Scales the given (x,y) coordinates to correspond with the indexing of
        # the DEM array.
        return (loc - self.origin) / self.step


    def range(self):
        # Returns two (x,y) points, one at either corner of the basin data.
        return self.origin, self.origin + self.step * self.zg.shape


    def surface(self, loc):
        # Returns the z coordinate on the ground surface at loc
        locI = self.locationToIndices(loc)
        if locI.shape == (2,):
            z = scipy.ndimage.map_coordinates(self.zg0, locI.reshape(2,1))
        else:
            z = scipy.ndimage.map_coordinates(self.zg0, locI.transpose())
        return z


    def loadStreams(self):

        streams = oo.Open('coweeta_streams/coweeta_streams.dbf')
        layer = streams.GetLayerByIndex(0)
        numFeat = layer.GetFeatureCount()

        self.streamSegs = range(numFeat)

        for i in range(numFeat):
            feat = layer.GetFeature(i)
            geomRef = feat.GetGeometryRef()
            self.streamSegs[i] = np.array(geomRef.GetPoints())


    def loadWatersheds(self):

        self.watershed = dict()
        sws = oo.Open('coweeta_subwatersheds/coweeta_subwatersheds.dbf')
        layer = sws.GetLayerByIndex(0)
        numFeat = layer.GetFeatureCount()

        jd = json.JSONDecoder()
        for i in range(numFeat):

            feat = layer.GetFeature(i)

            wsNum = feat.GetField(0)
            area = feat.GetField(1)/10000
            geoRef = feat.GetGeometryRef()

            geom = geoRef.ExportToJson()
            struct = jd.decode(geom)
            coords = struct['coordinates'][0]
            self.watershed[wsNum] = np.array(coords)


    def wsBoundary(self, wsNum):
        points = self.watershed[wsNum] - self.refPoint
        x = points[:,0]
        y = points[:,1]
        z = self.surface(points)
        return x, y, z




