import pygame
from pygame.locals import *

from retroSnake.pygText import *
from retroSnake.maths import *


def init(cap='retroSnake'):
    pygame.init()

    global screen
    screen = pygame.display.set_mode((640, 480))

    global scratch
    scratch = screen.copy()

    global caption
    caption = cap


def flipDisplay():
    pygame.display.update()


def quit():
    pygame.quit()


class Game(object):
    def __init__(self):
        global game
        game = self

    def run(self):
        physTime = 1000/40
        clock = pygame.time.Clock()
        accumulator = 0
        while True:
            for event in pygame.event.get():
                self.onEvent(event)

            clock.tick(0)
            pygame.display.set_caption('%s: %f' % (caption, clock.get_fps()))
            delta = clock.get_rawtime()
            accumulator += delta
            while accumulator >= physTime:
                accumulator -= physTime
                self.update()
            self.render(screen)

    def onEvent(self):
        return

    def update(self):
        return

    def render(self, screen):
        return

    def exit(self):
        quit()
        raise SystemExit


class Entity(object):
    def __init__(self):
        self.sprite = None
        self.transform = Matrix()

    def doTransform(self, matrix):
        self.transform = self.transform*matrix

    def setSprite(self, sprite):
        self.sprite = sprite

    def render(self, dest, transform):
        self.sprite.render(dest, self.transform, transform)

    def update():
        self.sprite.update()


class Camera():
    def __init__(self):
        self.transform = Matrix()
        self.scale = 12
        self.focus = Vector(0, 0)

    def buildMatrix(self):
        self.transform = Matrix()
        self.transform = self.transform*TranslateMatrix(320, 240)
        self.transform = self.transform*ScaleMatrix(self.scale)
        self.transform = self.transform*TranslateMatrix(self.focus)

    def unproject(self, p):
        return self.transform.inverse()*p


class Sprite(object):
    def __init__(self, v, n, t):
        self.verts = [Vector(*x) for x in v]
        self.ngons = n
        self.tris = t

        self.needTransform = False
        self.transform = Matrix()
        self.lastWorld = None
        self.tVerts = self.verts
        self.wVerts = self.verts
        self.sVerts = self.verts
        self.regenClips = True
        self.update()
        self.calculateTransform(True)

    def doTransform(self, matrix):
        self.transform = self.transform*matrix
        self.needTransform = True

    def calculateTransform(self, force=False):
        if self.needTransform or force:
            self.tVerts = [self.transform*v for v in self.verts]
            self.needTransform = False
            self.radius = sorted(self.tVerts, key=lambda x: x.hypotemuse)[0]

    def calculateBounds(self, world=None):
        if world is not None:
            self.wVerts = [(world*vertex) for vertex in self.tVerts]
        xMin = xMax = self.wVerts[0].getX()
        yMin = yMax = self.wVerts[0].getY()
        for vert in self.wVerts:
            if vert.getX() < xMin:
                xMin = vert.getX()
            elif vert.getX() > xMax:
                xMax = vert.getX()
            if vert.getY() < yMin:
                yMin = vert.getY()
            elif vert.getY() > yMax:
                yMax = vert.getY()
        self.bound = [
            xMin, xMax, yMin, yMax
        ]

    def update(self):
        if self.regenClips:
            clips = []
            for tri in self.tris:
                clips.append([self.wVerts[i] for i in tri])
            self.clips = clips
            self.regenClips = False
        self.calculateBounds()

    def render(self, dest, world, camera):
        self.calculateTransform()
        if self.lastWorld != world:
            self.wVerts = [(world*vertex) for vertex in self.tVerts]
            self.lastWorld = world
            self.regenClips = True
        self.sVerts = [(camera*vertex).data[:2] for vertex in self.wVerts]
        for ngon in self.ngons:
            ngon = [self.sVerts[i] for i in ngon]
            pygame.draw.polygon(dest, (0, 42, 0), ngon)
            pygame.draw.aalines(dest, (0, 255, 0), True, ngon)


loadedSprites = {}


def loadSprite(sprite, force=False):
    try:
        if not force:
            return loadCache(sprite)
    except KeyError:
        pass

    try:
        return loadRSO(sprite)
    except IOError:
        pass

    return None


def loadCache(sprite):
    vertices = loadedSprites[sprite][0]
    ngons = loadedSprites[sprite][1]
    tris = loadedSprites[sprite][2]
    print 'Loaded cached sprite: %s\n' % sprite
    return Sprite(vertices, ngons, tris)


def loadRSO(sprite):
    print 'Loading RSO sprite: %s' % sprite
    vertices = []
    ngons = []
    tris = []
    order = [('triangles', tris), ('n-gons', ngons), ('vertices', vertices)]

    with open('assets/%s.rso' % sprite) as f:
        print '\tFile opened.'
        if f.readline().strip() != '$rso$':
            return None
        else:
            print '\tPassed header check.'
        f.readline()

        print '\tLoading...'
        for line in f:
            line = line.strip()
            if line == '':
                old = order.pop()
                if old:
                    print '\t\tLoaded %d %s.' % (len(old[1]), old[0])
            elif order[-1][0] == 'vertices':
                order[-1][1].append([float(x) for x in line.split()])
            else:
                order[-1][1].append([int(x) for x in line.split()])

    print '\tChecking for validity...'
    score = 0
    if len(vertices) == 0:
        print '\t\tFailed: No vertices.\n'
    elif len(ngons) == 0:
        print '\t\tFailed: No ngons.\n'
    elif len(tris) == 0:
        print '\t\tFailed: No tris.\n'
    elif len(tris) != sum([len(ngon)-2 for ngon in ngons]):
        print '\t\tFailed: Wrong number of tris for given ngons.\n'
    else:
        print '\t\tSuccess.\n'
        loadedSprites[sprite] = []
        loadedSprites[sprite].append(vertices)
        loadedSprites[sprite].append(ngons)
        loadedSprites[sprite].append(tris)
        return Sprite(vertices, ngons, tris)
    return None
