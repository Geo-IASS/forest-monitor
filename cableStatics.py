

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
        self.solveParams()


    def cableZ(self, x):
        # Returns height of cable at vertical position x.
        return self.a * np.cosh((x + self.xc) / self.a) + self.zc


    def length(self):
        # Returns the total length of cable from start to end
        return (self.a * (np.sinh((self.w - self.x0) / self.a) - np.sinh((- self.xc) / self.a)))


    def verticalForce(self, x):
        # Returns a tuple containing the vertical component of tension at
        # vertical location x

        return np.sinh((x + self.xc) / self.a) * self.th


    def tension(self, x):
        # Returns a tuple containing the total tension at vertical location x
        fv = self.verticalForce(x)
        return np.sqrt(np.square(fv)  + np.square(self.th))


    def solveParams(self):
        # Given the specified values for w, z1 and z2, determine the offsets
        # xc and zc required to match a catenary to our cable.  This is done
        # algerbraically.  The deriviation of the equation was performed with
        # the sympy package.

        w = self.w
        a = self.a
        zd = self.z2 - self.z1

        # calculate some repeated elements
        e2wa = np.exp(2 * w / a)
        ewa = np.exp(w / a)
        a2 = a ** 2

        # calculate the 3 components
        c1 = (a2 * e2wa - 2 * a2 * ewa + a2 + zd ** 2 * ewa) * ewa
        c2 = (-2 * a * e2wa + 2 * a * ewa)
        c3 = zd / (a * (ewa - 1))

        # Determine the x offset ...
        self.xc = a * np.log(2 * np.abs(np.sqrt(c1) / c2) + c3)

        # ... and from this the y offset
        self.zc = self.z1 - a * np.cosh(self.xc / a)


    def setTension(self, ten, x):
        # Calculate the (uniform) horizontal component of tension in the cable
        # required to give a total tension of 'ten' at location 'x'.
        # Determined numerically using least squares.

        def error(th):
            self.setHorizForce(th)
            calcTen = self.tension(x)
            return ten - calcTen

        res = spipyopt.leastsq(error, [ten])
        self.th = res[0][0]




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



    def tensionAtMasts(self):
        return [self.c[i].tension(0) for i in range(3)]


    def simpleForces(self):
        # Compute the tensions required if massless cables were used.  This is a
        # starting point for computing the tensions for cables with mass.
        A = np.transpose(np.array([self.dirVec[0], self.dirVec[1], self.dirVec[2]]))
        b = np.array([0, 0, self.weight])
        tensions = np.linalg.solve(A,b)
        self.th = [tensions[i] * planMag(self.dirVec[i]) for i in range(3)]
        if min(self.th) < 0:
            raise RuntimeError('Negative tension')


    def setup(self):
        self.c = [0,0,0]
        for i in range(3):
            self.c[i] = Cable(self.p[i][2], self.pb[2], horizDist(self.p[i], self.pb), self.unitWeight)


    def tryth(self, k):
        for i in range(3):
            self.c[i].setHorizForce(self.th[i] * k)
            self.c[i].solveParams()

        vf = np.sum([self.c[i].verticalForce(self.c[i].w) for i in range(3)])
        error = self.weight + vf
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


