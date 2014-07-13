import math
import weakref
import itertools

import pygame


_display = "not initialised"
_actors = []
_queue = []


def init():
    """ Initialise retroSnake.

        returns True on success,
        returns False on failure """

    pygame.display.init()
    if not pygame.display.get_init():
        return False

    return True


def setupDisplay(width, height, caption):
    """ Set display properties. """
    global _display
    _display = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return _display


class Vector(object):
    """ 2D Vector class. """
    def __init__(self, x, y):
        self.data = (float(x), float(y), 1.0)

    def __str__(self):
        return "Vector: %s" % str(self.data)

    def __add__(self, x):
        v = Vector(self.data[0]+x.data[0],
                   self.data[1]+x.data[1])
        return v

    def __mul__(self, x):
        v = Vector(self.data[0]*x,
                   self.data[1]*x)
        return v

    def __div__(self, x):
        v = Vector(self.data[0]/x,
                   self.data[1]/x)
        return v


class Matrix(object):
    """ 2D Matrix class. """
    def __init__(self, data=None):
        if data is None:
            data = ((1, 0, 0),
                    (0, 1, 0),
                    (0, 0, 1))
        self.data = data

    def __str__(self):
        return "Matrix: %s" % str(self.data)

    def __mul__(self, x):
        if isinstance(x, Vector):
            data = []
            a = self.data
            b = x.data

            for x in range(2):
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
            for x in range(3):
                row = []
                for y in range(3):
                    tmp = []
                    tmp.append(a[x][0]*b[0][y])
                    tmp.append(a[x][1]*b[1][y])
                    tmp.append(a[x][2]*b[2][y])
                    row.append(sum(tmp))
                data.append(tuple(row))

            return Matrix(tuple(data))


class Point(object):
    def __init__(self, pos):
        self.pos = pos

    def draw(self, matrix=Matrix()):
        pos = matrix*self.pos
        pos = (int(pos.data[0]), int(pos.data[1]))
        pygame.draw.circle(_display, (0, 255, 0), pos, 3)


class Line(object):
    """ Line object. """
    def __init__(self, v1, v2):
        self.start = v1
        self.end = v2

    def draw(self, matrix=Matrix()):
        v1 = matrix*self.start
        v2 = matrix*self.end
        pygame.draw.aaline(_display, (0, 255, 0), v1.data[:2], v2.data[:2])

    def setWorld(self, matrix):
        self.world = matrix


class LineLoop(object):
    """ LineLoop object. """
    def __init__(self, *vertices):
        self.vertices = vertices

    def draw(self, matrix=Matrix()):
        verts = [(matrix*v).data[:2] for v in self.vertices]
        pygame.draw.aalines(_display, (0, 255, 0), True, verts)

    def setWorld(self, matrix):
        self.world = matrix


class Polygon(object):
    def __init__(self, *vertices):
        self.vertices = vertices

    def draw(self, matrix=Matrix()):
        verts = [(matrix*v).data[:2] for v in self.vertices]
        pygame.draw.polygon(_display, (0, 42, 0), verts)
        pygame.draw.aalines(_display, (0, 255, 0), True, verts)

    def setWorld(self, matrix):
        self.world = matrix


class Sprite(object):
    """ Sprite object. """
    def __init__(self, lines=[]):
        self.lines = lines[:]
        self.local = Matrix()
        self.world = Matrix()

    def setLocalMatrix(self, matrix):
        self.local = matrix

    def getLocalMatrix(self):
        return self.local

    def applyLocalMatrix(self, matrix):
        self.local *= matrix

    def setWorldMatrix(self, matrix):
        self.world = matrix

    def getWorldMatrix(self):
        return self.world

    def applyWorldMatrix(self, matrix):
        self.world *= matrix

    def draw(self, view=Matrix()):
        matrix = self.world*self.local
        matrix = view*matrix
        for line in self.lines:
            line.draw(matrix)


def newScaleMatrix(factor):
    """ Create a new scaling matrix. """
    f = float(factor)
    data = ((f, 0, 0),
            (0, f, 0),
            (0, 0, 1))
    return Matrix(data)


def newRotateMatrix(angle):
    """ Create a new rotation matrix. """
    f = float(angle)
    s = math.sin(angle)
    c = math.cos(angle)
    data = ((c, -s, 0),
            (s, c, 0),
            (0, 0, 1))
    return Matrix(data)


def newTranslateMatrix(dx, dy):
    """ Create a new translation matrix. """
    data = ((1, 0, dx),
            (0, 1, dy),
            (0, 0, 1))
    return Matrix(data)


class World(object):
    """ World class, represents a scene. """
    def __init__(self):
        self.sprites = []

    def addSprite(self, sprite):
        self.sprites.append(sprite)

    def removeSprite(self, sprite):
        self.sprites.remove(sprite)

    def update(self, sprite):
        pass


class Camera(object):
    def __init__(self, world):
        self.world = world
        self.matrix = Matrix()

    def setMatrix(self, matrix):
        self.matrix = matrix

    def getMatrix(self, matrix):
        return self.matrix

    def applyMatrix(self, matrix):
        self.matrix *= matrix

    def draw(self):
        for sprite in self.world.sprites:
            sprite.draw(self.matrix)


if __name__ == "__main__":
    print "This is a library file."
