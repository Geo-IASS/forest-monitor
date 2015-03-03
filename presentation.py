
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cm

import numpy as np

import cableStatics as cs


def new3d():
    plt.figure(figsize=(12,8))
    ax = plt.subplot(111, projection='3d') # , aspect='equal')
    plt.xlabel('metres E-W')
    plt.ylabel('metres N-S')
    return ax



def showExampleSystem3d():
    # Position the 3 anchor points at 200m from each other and at 10m high.  Specify 350mN/m cable (2.4lb/100ft)
    tcs = cs.TriCableSystem([[0, 0, 10], [0, 200, 10], [150, 100, 10]], 0.35)

    # Position the platform at 5m and set its weight at 100N
    tcs.setLoad([75, 100, 5], 100)

    # Adjust cable tension to achieve desired location.
    tcs.tune()

    # Display
    ax = cs.new3d()

    tree(ax, 100, 200, 0, 4)
    tree(ax, 80, 150, 0, 3)
    tree(ax, 20, 100, 0, 3)
    tree(ax, 140, -20, 0, 2)

    mast(ax, 0, 0, 0, 10)
    mast(ax, 0, 200, 0, 10)
    mast(ax, 150, 100, 0, 10)

    showTcsCables(ax, tcs)
    cs.report(tcs, 3, ax)

    ax.plot([tcs.pb[0], tcs.pb[0]], [tcs.pb[1], tcs.pb[1]], [tcs.pb[2], tcs.pb[2]-3], 'b')
    ax.plot([tcs.pb[0], tcs.pb[0]], [tcs.pb[1], tcs.pb[1]], [tcs.pb[2], tcs.pb[2]-3], 'ro')

    ax.set_title('Example Canopy Cable Suspended Robot')


def showTcsCables3d(ax, tcs):

    for i in range(3):
        x = np.linspace(tcs.pb[0], tcs.p[i][0], 50)
        y = np.linspace(tcs.pb[1], tcs.p[i][1], 50)
        d = np.linspace(0, tcs.c[i].w, 50)
        z = tcs.c[i].cableZ(d)
        ax.plot([tcs.pb[0], tcs.p[i][0]], [tcs.pb[1], tcs.p[i][1]], [0, 0], 'g')
        ax.plot(x, y, z, 'b')


def showTcsCables2d(ax, tcs):

    for i in range(3):
        ax.plot([tcs.pb[0], tcs.p[i][0]], [tcs.pb[1], tcs.p[i][1]], 'g')
        ax.plot([tcs.p[i][0]], [tcs.p[i][1]], 'ro')
        ax.text(tcs.p[i][0], tcs.p[i][1], 'M{}'.format(i+1))
    ax.plot([tcs.pb[0]], [tcs.pb[1]], 'ro')




def showInstallation3d(ax, itcs, nwLoc, swLoc):
    x, y, z = itcs.terrain.surfaceMesh(nwLoc, swLoc)
    ax.contour(x, y, z, 20, cmap=cm.coolwarm)

    ax.plot_surface(x, y, z, rstride=20, cstride=20, alpha=0.3, linewidth=0)

    x, y, z = itcs.terrain.wsBoundary(18)

    ax.plot(x, y, z,'r')

    for i in range(3):
        mast(ax, itsc.mastX[i], itsc.mastY[i], itsc.mastBaseZ[i], itsc.mastTopZ[i])

    showTcsCables(ax, itsc.tsc)


def showInstallation2d(ax, itcs, nwLoc, swLoc):
    x, y, z = itcs.terrain.surfaceMesh(nwLoc, swLoc)
    ax.contour(x, y, z, 20, cmap=cm.coolwarm)
    x, y, z = itcs.terrain.wsBoundary(18)

    ax.plot(x, y, 'k')

    showTcsCables2d(ax, itcs.tcs)


def mast(ax, x, y, zb, zt):
    # draws a tapered mast symbol at x,y rising from zb to zt
    xa = np.array([0, -1, -1,  0,  1,  1,  0]) + x
    ya = np.array([0,  1, -1,  0, -1,  1,  0]) + y
    za = np.array([1,  0,  0,  1,  0,  0,  1]) * (zt - zb) + zb
    ax.plot(xa, ya, za, 'r')


def tree(ax, xc, yc, zb, h):
    # draw a helical coniferous thing
    a = np.linspace(0, 1, 200)
    x, y = xc + 5 * a * np.sin(a * 20 * np.pi), yc + 5 * a * np.cos(a * 20 * np.pi)
    z = zb + h - h * a * 0.8
    ax.plot(x, y, z, 'g')
    ax.plot([xc, xc], [yc, yc], [zb, zb + h * 0.8], 'r')



