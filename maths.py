import math
import random


class Vector(object):
    """ 2D Vector class. """
    def __init__(self, x, y):
        x, y = round(float(x), 5), round(float(y), 5)
        self.data = (x, y, 1.0)
        t = self.data[0]*self.data[0] + self.data[1]*self.data[1]
        self.hypotemuse = math.sqrt(t)

    def __str__(self):
        return "Vector: %s" % str(self.data[:2])

    def __repr__(self):
        return self.__str__()

    def __add__(self, x):
        v = Vector(self.data[0]+x.data[0],
                   self.data[1]+x.data[1])
        return v

    def __eq__(self, x):
        return self.data[0] == x.data[0] and \
            self.data[1] == x.data[1]

    def __sub__(self, x):
        v = Vector(self.data[0]-x.data[0],
                   self.data[1]-x.data[1])
        return v

    def __mul__(self, x):
        v = Vector(self.data[0]*x,
                   self.data[1]*x)
        return v

    def __div__(self, x):
        v = Vector(self.data[0]/x,
                   self.data[1]/x)
        return v

    def normalised(self):
        h = self.hypotemuse
        if h != 0:
            v = Vector(self.data[0]/h, self.data[1]/h)
        else:
            v = self
        return v

    def cross(self, x):
        return self.data[0]*x.data[1] -\
            self.data[1]*x.data[0]

    def dot(self, x):
        return self.data[0]*x.data[0] +\
            self.data[1]*x.data[1]

    def getX(self):
        return self.data[0]

    def getY(self):
        return self.data[1]


class Matrix(object):
    """ 2D Matrix class. """
    def __init__(self, data=None):
        if data is None:
            data = ((1, 0, 0),
                    (0, 1, 0),
                    (0, 0, 1))
        self.data = data

        a, b, c = data[0][0], data[0][1], data[0][2]
        d, e, f = data[1][0], data[1][1], data[1][2]
        g, h, i = data[2][0], data[2][1], data[2][2]
        self.determinant = (a*(e*i-f*h)) - (d*(b*i-c*h)) + (g*(b*f-c*e))

    def __str__(self):
        return "Matrix: %s" % str(self.data)

    def __eq__(self, x):
        for a, b in zip(self.data, x.data):
            for a, b in zip(x, y):
                if x != y:
                    return False
        return True

    def __mul__(self, x):
        if isinstance(x, Vector):
            data = []
            a = self.data
            b = x.data

            for x in xrange(2):
                tmp = []
                tmp.append(a[x][0]*b[0])
                tmp.append(a[x][1]*b[1])
                tmp.append(a[x][2]*b[2])
                data.append(sum(tmp))

            return Vector(*data)
        elif isinstance(x, Matrix):
            data = []
            a = self.data
            b = x.data

            row = []
            for x in xrange(3):
                row = []
                for y in xrange(3):
                    tmp = []
                    tmp.append(a[x][0]*b[0][y])
                    tmp.append(a[x][1]*b[1][y])
                    tmp.append(a[x][2]*b[2][y])
                    row.append(sum(tmp))
                data.append(tuple(row))

            return Matrix(tuple(data))
        else:
            data = []
            for row in self.data:
                tmp = []
                for item in row:
                    tmp.append(item*x)
                data.append(tuple(tmp))
            return Matrix(tuple(data))

    def transpose(self):
        d = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]
        for i in xrange(3):
            for j in xrange(3):
                d[i][j] = self.data[j][i]
        return Matrix(d)

    def inverse(self):
        if self.determinant == 0:
            return None
        data = self.data
        a, b, c = data[0][0], data[0][1], data[0][2]
        d, e, f = data[1][0], data[1][1], data[1][2]
        g, h, i = data[2][0], data[2][1], data[2][2]

        dat = ((e*i-f*h, c*h-b*i, b*f-c*e),
               (f*g-d*i, a*i-c*g, c*d-a*f),
               (d*h-e*g, b*g-a*h, a*e-b*d))

        return Matrix(dat) * (1/self.determinant)


class ScaleMatrix(Matrix):
    """ Create a new scaling matrix. """
    def __init__(self, factor):
        f = float(factor)
        data = ((f, 0, 0),
                (0, f, 0),
                (0, 0, 1))
        Matrix.__init__(self, data)


class RotateMatrix(Matrix):
    """ Create a new rotation matrix. """
    def __init__(self, angle):
        f = float(angle)
        s = math.sin(angle)
        c = math.cos(angle)
        data = ((c, -s, 0),
                (s, c, 0),
                (0, 0, 1))
        Matrix.__init__(self, data)


class TranslateMatrix(Matrix):
    """ Create a new translation matrix. """
    def __init__(self, a, b=None):
        if b is None:
            self.fromVector(a)
        else:
            self.fromComponents(a, b)

    def fromVector(self, v):
        self.fromComponents(v.data[0], v.data[1])

    def fromComponents(self, x, y):
        data = ((1, 0, x),
                (0, 1, y),
                (0, 0, 1))
        Matrix.__init__(self, data)


def getIntersection(v0, v1, v2, v3):
    p, q = v0, v2
    r, s = (v1-v0), (v3-v2)

    rs = r.cross(s)
    if rs == 0:
        if (q-p).cross(r) != 0:
            return False
        if (q-p).dot(r) <= r.dot(r):
            return True
        if 0 <= (p-q).dot(s) <= s.dot(s):
            return True
        return False

    t = (q-p).cross(s/rs)
    u = (q-p).cross(r/rs)

    if rs != 0 and \
       0 <= t <= 1 and \
       0 <= u <= 1:
        return p + r*t
    else:
        return False


# Helper for getSameSide, determines cross product of vectors
def GSS_cross(v0, v1):
    x = v0[1]*v1[2] - v1[1]*v0[2]
    y = v0[2]*v1[0] - v1[2]*v0[0]
    z = v0[0]*v1[1] - v1[0]*v0[1]
    return [x, y, z]


# Helper for getSameSide, determines dot product of vectors
def GSS_dot(v0, v1):
    x = v0[0]*v1[0]
    y = v0[1]*v1[1]
    z = v0[2]*v1[2]
    return x+y+z


# Determine if a and b are on the same side of line segment v0->v1
def getSameSide(v0, v1, a, b):
    # Note: This function uses an internal format for processing.
    t0 = list((b-a).data[:2]) + [0.0]
    t1 = list((v0-a).data[:2]) + [0.0]
    t2 = list((v1-a).data[:2]) + [0.0]
    c0 = GSS_cross(t0, t1)
    c1 = GSS_cross(t0, t2)
    if GSS_dot(c0, c1) <= 0:
        return True
    else:
        return False


# Determine if x is within the triangle of vectors
def inTriangle(v0, v1, v2, x):
    a = getSameSide(v0, v1, v2, x)
    b = getSameSide(v0, v2, v1, x)
    c = getSameSide(v1, v2, v0, x)
    return (a and b and c)


# This probably belogs here, expects rects in format of:
#   [xMin, xMax, yMin, yMax]
def overlap(a, b):
    left = lambda r: r[0]
    right = lambda r: r[1]
    top = lambda r: r[2]
    bottom = lambda r: r[3]

    retVal = True and not right(a) < left(b)
    retVal = retVal and not left(a) > right(b)
    retVal = retVal and not bottom(a) < top(b)
    retVal = retVal and not top(a) > bottom(b)

    return retVal


def rand(m, M):
    r = random.random()
    r *= M-m
    r += m
    return r
