# class Point:
    # def __init__Point(self, x, y, z):
        # self.x = x
        # self.y = y
        # self.z = z
#
#
#
# def angles(p):
    # thetaH = math.atan2(p[1], p[0])
    # thetaV = math.atan2(p[2], math.sqrt(p[1]^2 + p[0]^2))
    #
    # return thetaH, thetaV
#
# def p(x,y,z):
    # return np.array([x,y,z])
#
#
# def mag(p1):
        # return np.sqrt(np.sum(p1 * p1))
        #
        #
        #
# def forces(p1, p2, p3):
    # A = np.transpose(np.array([p1 / mag(p1), p2 / mag(p2), p3 / mag(p3)]))
    # b = np.array([0,0,1])
    # return np.linalg.solve(A,b)
#
#
#
# a = 4000
# h = 1
# w = 100
# def catenary(x, a):
    # return a * np.cosh(x/a)
#
# def cable(x0, a, w, h):
    # return catenary(x0, a) + h - catenary(w+x0, a)
#
#
# res = leastsq(cable,[0], (4000, 100, 10))
# x0 = res[0][0]
# x0
# y0 = catenary(x0, 4000)
# x0, y0
# catenary(x0, 4000)-y0,catenary(x0+100, 4000)-y0
#
#
# x = np.arange(0, w, 0.01)
# y = catenary(x+x0, a)-y0
# plt.plot(x,y)
# plt.show()



import numpy as np
import scipy.optimize as spipyopt

class Cable:
    # Model of a static cable suspended at each each.  The cable follows the
    # catenary curve.  The horizontal component of tension, th, is uniform along
    # the cable length.

    def __init__(self, z1, z2, w, unitWeight):
        # Specify the height of the cable at each end and the vertical distance
        # between those ends.  Also specify the weight (force due to gravity,
        # not mass) of the cable per unit length (e.g. N/m).
        self.z1 = z1
        self.z2 = z2
        self.w = w
        self.unitWeight = unitWeight


    def setHorizForce(self, th):
        # Specify the horizontal component of the cable tension (which will be
        # constant along the cable length.
        self.th = th
        self.a = th / self.unitWeight


    def cableZ(self, x):
        # Returns height of cable at vertical position x.
        return self.a * np.cosh((x - self.x0) / self.a) - self.z0


    def length(self):
        # Returns the total length of cable from start to end
        return (self.a * (np.sinh((self.w - self.x0) / self.a) - np.sinh((- self.x0) / self.a))).flatten()


    def verticalForce(self):
        # Returns a tuple containing the vertical component of tension at the two
        # ends of the cable
        return np.sinh(-self.x0 / self.a) * self.th, -np.sinh((self.w - self.x0) / self.a) * self.th


    def tension(self):
        # Returns a tuple containing the total tension at the two ends of the cable
        fv = self.verticalForce()
        return np.sqrt(np.square(fv)  + np.square(self.th)).flatten()


    def cableError(self, x):
        # Used by solveParams() to establish offsets.  For the right x value
        # the return value will be zero.
        return (self.cableZ(x) - self.z1) - (self.cableZ(x + self.w) - self.z2)


    def solveParams(self):
        # Determine the vertical and horizontal offsets needed to map the catenary
        # equation onto our cable.  Uses least squares estimation.
        self.x0 = 0
        self.z0 = 0
        res = spipyopt.leastsq(self.cableError,[0])
        # print res
        self.x0 = -res[0][0]
        self.z0 = self.cableZ(0) - self.z1

#    def solveForTension(self, t):
#        # th is a function of net tension at the point and the gradient of the cable
#
#        # dz/dx = sinh(x/a) = sinh(x . w /th)
#
#        z1, z2, w, t1
#
#        need th


def planMag(v):
    # The magnitude of the 3D vector v in the horizontal plane.  I.e. result is
    # 0 if the vector points straight up.
    return np.sqrt(np.square(v[0]) + np.square(v[1]))


def horizDist(p1, p2):
    # What's the distance between the two points, neglecting the altitude
    # component?
    return planMag(p1 - p2)


def dist(p1, p2):
    # What's the line of sight distance between two points, including height
    # differences.
    return np.sqrt(np.sum(np.square(p1 - p2)))


def mag(p):
    pn = np.array(p)
    return np.sqrt(np.sum(pn * pn))


def dirVec(p1, p2):
    # returns unit vector pointing in the same direction as from p1 to p2.
    return (p2 - p1) / mag(p2 - p1)


def planVec(dv):
    return [dv(0), dv(1)] / planMag(dv);


class TriCableSystem:
    # In which a movable load is suspended by three cables, each run from a
    # separate fixed anchor point.  Dynamic effects are not considered.  The
    # weight of the cables are factored in.

    def __init__(self, anchors, unitWeight):
        # Where anchors is a three element list, each element is a numpy array
        # giving a point in space, (x, y and z).

        self.p = anchors
        self.unitWeight = unitWeight


    def setLoad(self, pb, weight):
        # Place a weight (force) at position pb
        self.pb = np.array(pb)
        self.weight = weight

        # The horizonal direction vectors are fixed.
        self.dirVec = [dirVec(self.pb, self.p[i]) for i in range(3)]

        #TEMP!!! print 'dir vec: ', self.dirVec


    def simpleForces(self):
        A = np.transpose(np.array([self.dirVec[0], self.dirVec[1], self.dirVec[2]]))
        #cableL = np.sum(dist(self.pb, self.p))
        #cableW = cableL * self.unitWeight;
        b = np.array([0, 0, self.weight]) # + cableW / 2])
        tensions = np.linalg.solve(A,b)
        self.th = [tensions[i] * planMag(self.dirVec[i]) for i in range(3)]
                   # planVec
        #TEMP!!! print 'tensions: ', tensions
        #TEMP!!! print 'ten horiz: ', self.th
        # print 'ten x: ', [tensions[i] * self.dirVec[i][0] for i in range(3)]
        # print 'ten x: ', [tensions[i] * self.dirVec[i][1] for i in range(3)]
        #TEMP!!! print 'ten h x: ', [self.th[i] * self.dirVec[i][0]/planMag(self.dirVec[i]) for i in range(3)]
        #TEMP!!! print 'ten h y: ', [self.th[i] * self.dirVec[i][1]/planMag(self.dirVec[i]) for i in range(3)]


    def setup(self):
        self.c = [0,0,0]
        for i in range(3):
            self.c[i] = Cable(self.pb[2], self.p[i][2], horizDist(self.pb, self.p[i]), self.unitWeight)


    def tryth(self, k):
        for i in range(3):
            self.c[i].setHorizForce(self.th[i] * k)
            self.c[i].solveParams()

        #print 'length: ', [self.c[i].length() for i in range(3)]
        #print 'tension at towers: ', [self.c[i].tension()[1] for i in range(3)]
        vf = np.sum([self.c[i].verticalForce()[0] for i in range(3)])
        #print 'vert forces: ', [self.c[i].verticalForce()[0] for i in range(3)]
        error = self.weight - vf
        #print 'error: ', error
        return error


    def tune(self):
        self.simpleForces()
        self.setup()

        res = spipyopt.leastsq(self.tryth, [1])
        k = res[0][0]
        self.th *= k


    def getStatus(self):
        # returns th, tension, cable length
        return



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from presentation import tower

def new3d():
    ax = plt.subplot(111, projection='3d')
    ax.set_xlabel('metres E-W [m]')
    ax.set_ylabel('metres N-S [m]')
    ax.set_zlabel('height [m]')
    return ax

def report(tcs, bobDrop=0, ax=None):
    doAll = not(ax)
    if doAll:
        ax = plt.subplot(111, projection='3d')

    for i in range(3):
        x = np.linspace(tcs.pb[0], tcs.p[i][0], 50)
        y = np.linspace(tcs.pb[1], tcs.p[i][1], 50)
        d = np.linspace(0, tcs.c[i].w, 50)
        z = tcs.c[i].cableZ(d)
        ax.plot([tcs.pb[0], tcs.p[i][0]], [tcs.pb[1], tcs.p[i][1]], [0, 0], 'g')
        tower(tcs.p[i][0], tcs.p[i][1], 0, tcs.p[i][2], ax)
        ax.plot(x, y, z, 'b')
    if bobDrop:
        ax.plot([tcs.pb[0], tcs.pb[0]], [tcs.pb[1], tcs.pb[1]], [tcs.pb[2], tcs.pb[2]-bobDrop], 'b')
        ax.plot([tcs.pb[0], tcs.pb[0]], [tcs.pb[1], tcs.pb[1]], [tcs.pb[2], tcs.pb[2]-bobDrop], 'ro')
    else:
        ax.plot([tcs.pb[0]], [tcs.pb[1]], [tcs.pb[2]], 'ro')

    ax.set_xlabel('EW direction [m]')
    ax.set_ylabel('NS direction [m]')
    ax.set_zlabel('Height [m]')

    if doAll:
        plt.show()


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


def tensionMap(tcs, res, ter, load, thresh):

    import matplotlib.path as mplp

    def roundRange(vals, res):
        start = np.floor(np.min(vals) / res) * res
        end = np.ceil(np.max(vals) / res) * res
        return np.arange(start, end + res / 2, res)


    xr = roundRange([tcs.p[i][0] for i in range(3)], res)
    yr = roundRange([tcs.p[i][1] for i in range(3)], res)

    bp = np.array([[tcs.p[i][j] for j in range(2)] for i in range(3)])
    # print(bp)
    bounds = mplp.Path(bp, np.array([1, 2, 2], dtype='uint8'), closed=True)

    ten = [np.ones((yr.size, xr.size)) * np.NaN for i in range(3)]

    for xi in range(len(xr)):
        x = xr[xi]
        for yi in range(len(yr)):
            y = yr[yi]
            p = (x,y)
            if bounds.contains_point(p):
                z = ter.surface(p) + 2
                tcs.setLoad((x,y,z), load)
                tcs.tune()
                if max([tcs.c[i].tension()[1] for i in range(3)]) < thresh:
                    for i in range(3):
                        ten[i][yi,xi] = tcs.c[i].tension()[1]


    x,y = np.meshgrid(xr, yr)
    # print x.shape, y.shape, ten[0].shape
    ax = plt.subplot(111, projection='3d')
    ax.plot_wireframe(x, y, ten[0], color='r')
    ax.plot_wireframe(x, y, ten[1], color='g')
    ax.plot_wireframe(x, y, ten[2], color='b')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()



