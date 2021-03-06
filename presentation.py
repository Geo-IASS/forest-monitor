
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cm

import numpy as np

import cableStatics as cs

from IPython.display import display, HTML



def new3d():
    plt.figure(figsize=(12,8))
    ax = plt.subplot(111, projection='3d') # , aspect='equal')
    ax.set_xlabel('metres E-W')
    ax.set_ylabel('metres N-S')
    ax.set_zlabel('elevation [m]')

    return ax



def showExampleSystem3d():
    # Position the 3 anchor points at 200m from each other and at 10m high.  Specify 350mN/m cable (2.4lb/100ft)
    tcs = cs.TriCableSystem([[0, 0, 10], [0, 200, 10], [150, 100, 10]], 0.35)

    # Position the platform at 5m and set its weight at 100N
    tcs.setLoad([75, 100, 5], 100)

    # Adjust cable tension to achieve desired location.
    if not tcs.tune():
        raise RuntimeError('Not all cables in tension')

    # Display
    ax = new3d()

    tree(ax, 100, 200, 0, 4)
    tree(ax, 80, 150, 0, 3)
    tree(ax, 20, 100, 0, 3)
    tree(ax, 140, -20, 0, 2)

    mast(ax, 0, 0, 0, 10)
    mast(ax, 0, 200, 0, 10)
    mast(ax, 150, 100, 0, 10)

    showTcsCables3d(ax, tcs)
    #TEMP!!! cs.report(tcs, 3, ax)

    ax.plot([tcs.pb[0], tcs.pb[0]], [tcs.pb[1], tcs.pb[1]], [tcs.pb[2], tcs.pb[2]-3], 'b')
    ax.plot([tcs.pb[0], tcs.pb[0]], [tcs.pb[1], tcs.pb[1]], [tcs.pb[2], tcs.pb[2]-3], 'ro')

    ax.set_title('Example Canopy Cable Suspended Robot')


def showCable(cable, ax=None):
    doAll = not(ax)
    if doAll:
        ax = plt.subplot(111)
        ax.set_title('Suspended Cable')
    x = np.linspace(0, cable.w, 50)
    z = cable.cableZ(x)
    ax.plot([0, cable.w], [cable.z1, cable.z2], 'ro')
    ax.plot(x,z,'b-')
    if doAll:
        plt.show()


def showTcsCables3d(ax, tcs):

    for i in range(3):
        x = np.linspace(tcs.p[i][0], tcs.pb[0], 50)
        y = np.linspace(tcs.p[i][1], tcs.pb[1], 50)
        d = np.linspace(0, tcs.c[i].w, 50)
        z = tcs.c[i].cableZ(d)
        ax.plot([tcs.pb[0], tcs.p[i][0]], [tcs.pb[1], tcs.p[i][1]], [0, 0], 'g')
        ax.plot(x, y, z, 'b')


def showTcsCables2d(ax, tcs, showPlat=False):
    if showPlat:
        for i in range(3):
            ax.plot([tcs.pb[0], tcs.p[i][0]], [tcs.pb[1], tcs.p[i][1]], 'g')
        ax.plot([tcs.pb[0]], [tcs.pb[1]], 'ro')

    for i in range(3):
        ax.plot([tcs.p[i][0]], [tcs.p[i][1]], 'ro')
        ax.text(tcs.p[i][0], tcs.p[i][1], 'mast {}'.format(i+1))




def showInstallation3d(ax, itcs, nwLoc, swLoc):
    x, y, z = itcs.terrain.surfaceMesh(nwLoc, swLoc)
    ax.contour(x, y, z, 20, cmap=cm.coolwarm)

    ax.plot_surface(x, y, z, rstride=20, cstride=20, alpha=0.3, linewidth=0)

    x, y, z = itcs.terrain.wsBoundary(18)

    ax.plot(x, y, z,'r')

    for i in range(3):
        mast(ax, itsc.mastX[i], itsc.mastY[i], itsc.mastBaseZ[i], itsc.mastTopZ[i])

    showTcsCables(ax, itsc.tsc)


def showInstallation2d(ax, itcs, nwLoc, swLoc, showPlat=False):
    x, y, z = itcs.terrain.surfaceMesh(nwLoc, swLoc)
    con = ax.contour(x, y, z, 20, cmap=cm.coolwarm)
    cb = plt.colorbar(con, shrink=0.6, extend='both')
    cb.set_label('Elevation [m]')

    def show(fn, ind, form):
        x, y, xc, yc = fn(ind)
        ax.plot(x, y, 'k')
        ax.text(xc, yc, form.format(ind), horizontalalignment='center', verticalalignment='center')


    show(itcs.terrain.wsMapCoords, 18, 'WS{}')

    for gp in [118, 218, 318]:
        show(itcs.terrain.gpMapCoords, gp, '{}')


    ax.set_xlabel('metres east of local reference')
    ax.set_ylabel('metres north of local reference')

    showTcsCables2d(ax, itcs.tcs, showPlat)



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



def coweetaMap():

    import coweeta
    plt.figure(figsize=(14,10))
    ax = plt.subplot(111)

    cow = coweeta.Coweeta()
    cow.loadWatersheds()
    cow.loadStreams()
    cow.setWorkingRefPoint((277000, 3880000))

    x, y, z = cow.surfaceMesh((-1e9, -1e9), (1e9, 1e9))
    con = ax.contourf(x, y, z, 20, cmap=cm.coolwarm)
    cb = plt.colorbar(con, shrink=0.6, extend='both')
    cb.set_label('Elevation [m]')

    def show(fn, ind, form, fill=False):
        x, y, xc, yc = fn(ind)
        if fill:
            ax.fill(x, y, facecolor='red', alpha=0.5)


        ax.plot(x, y, 'k')
        ax.text(xc, yc, form.format(ind), horizontalalignment='center', verticalalignment='center')


    for s in cow.streamSegs:

        x = s[:,0] - cow.refPoint[0]
        y = s[:,1] - cow.refPoint[1]
        ax.plot(x, y,'b')

    for w in cow.watershed.keys():
        show(cow.wsMapCoords, w, 'WS{}', w==18)

    ax.set_title('Coweeta Basin')

    ax.set_xlabel('metres east of local reference')
    ax.set_ylabel('metres north of local reference')




def tcsMapAll(xr, yr, zCeil, zFloor, zGround, floorTen, ceilTen, itcs):

    gridRes = xr[1] - xr[0]
    colHigh = zCeil - zGround
    valid = np.isfinite(colHigh)
    area = np.count_nonzero(valid) * gridRes ** 2
    volume = np.sum(colHigh[valid]) * gridRes ** 2
    s = '''<table>
    <tr><th>Accessible ground area</th><td>{:,} $m^2$</td></tr>
    <tr><th>Accessible airspace volume</th><td>{:,} $m^3$</td></tr>
    '''.format(int(area), int(volume))
    display(HTML(s))

    def tcsMap(title, arg):
        plt.figure(figsize=(14,10))

        ax = plt.subplot(111, aspect='equal')
        showInstallation2d(ax, itcs, [200,700], [1300,1500])

        cs = plt.contourf(xr, yr, arg)

        ax.set_title(title)

        cb = plt.colorbar(cs, shrink=0.6)
        cb.set_label(title)

    tcsMap('Maximum Elevation of Platform [m]', zCeil)
    tcsMap('Minimum Safe Elevation of Platform [m]', zFloor)
    tcsMap('Height Range of Platform [m]', zCeil - zFloor)
    tcsMap('Maximum Height of Platform Above Canopy [m]', zCeil - zGround)
    tcsMap('Minimum Safe Height of Platform Above Canopy [m]', zFloor - zGround)
    for i in range(3):
        title = 'Cable {0} Tension To Hold Platform At Minimum Elevation [N]'.format(i + 1)
        tcsMap(title, floorTen[:,:,i])

    tcsMap('Maximum Cable Tension To Hold Platform At Minimum Elevation [N]', np.max(floorTen, axis=2))


