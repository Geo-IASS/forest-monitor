
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

import cableStatics as cs

def showExampleSystem():
    # Position the 3 anchor points at 200m from each other and at 10m high.  Specify 350mN/m cable (2.4lb/100ft)
    tcs = cs.TriCableSystem([[0, 0, 10], [0, 200, 10], [150, 100, 10]], 0.35)

    # Position the platform at 5m and set its weight at 100N
    tcs.setLoad([75, 100, 5], 100)

    # Adjust cable tension to achieve desired location.
    tcs.tune()

    # Display
    plt.figure(figsize=(12,8))
    ax = cs.new3d()
    tree(100, 200, 0, 4, ax)
    tree(80, 150, 0, 3, ax)
    tree(20, 100, 0, 3, ax)
    tree(140, -20, 0, 2, ax)
    cs.report(tcs, 3, ax)
    ax.set_title('Example Canopy Cable Suspended Robot')
    plt.show()





def tower(x, y, zb, zt, ax):
    # draws a tapered tower symbol at x,y rising from zb to zt
    xa = np.array([0, -1, -1,  0,  1,  1,  0]) + x
    ya = np.array([0,  1, -1,  0, -1,  1,  0]) + y
    za = np.array([1,  0,  0,  1,  0,  0,  1]) * (zt - zb) + zb
    ax.plot(xa, ya, za, 'r')


def tree(xc, yc, zb, h, ax):
    # draw a helical coniferous thing
    a = np.linspace(0, 1, 200)
    x, y = xc + 5 * a * np.sin(a * 20 * np.pi), yc + 5 * a * np.cos(a * 20 * np.pi)
    z = zb + h - h * a * 0.8
    ax.plot(x, y, z, 'g')
    ax.plot([xc, xc], [yc, yc], [zb, zb + h * 0.8], 'r')



def showWs18():

    import json
    geom = ws18.ExportToJson()

    jd = json.JSONDecoder()

    struct = jd.decode(geom)


    gfr = ws18.GetGeomFieldRef(0)
    env = gfr.GetEnvelope()

    xc = (env[1] + env[0]) / 2
    w = (env[1] - env[0])
    yc = (env[3] + env[2]) / 2
    h = (env[3] - env[2])

    print w, h


    c.map([xc-w, yc-h],[xc+w, yc+h])

    x, y = [[ss[i] for ss in s['coordinates'][0]] for i in [0,1]]

    plt.plot(x,y,'k')
    plt.show()

