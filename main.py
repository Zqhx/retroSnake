import random
import retroSnake
from retroSnake import pygame


class Ship(object):
    def __init__(self, world):
        self.sprite = retroSnake.Sprite([
            retroSnake.Polygon(
                retroSnake.Vector(0, -15),
                retroSnake.Vector(10, 15),
                retroSnake.Vector(-10, 15),
                )
            ])
        self.world = world
        self.bullets = []

        world.addSprite(self.sprite)

    def handle(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(self.world, self, retroSnake.Vector(0, -15))
            self.bullets.append((pygame.time.get_ticks(), bullet))

    def update(self):
        keys = pygame.key.get_pressed()
        rotSpeed = .1
        if keys[pygame.K_w]:
            self.sprite.applyLocalMatrix(retroSnake.newTranslateMatrix(0, -5))
        if keys[pygame.K_s]:
            self.sprite.applyLocalMatrix(retroSnake.newTranslateMatrix(0, 0))
        if keys[pygame.K_a]:
            self.sprite.applyLocalMatrix(retroSnake.newRotateMatrix(-rotSpeed))
        if keys[pygame.K_d]:
            self.sprite.applyLocalMatrix(retroSnake.newRotateMatrix(rotSpeed))
        tick = pygame.time.get_ticks()
        dead = [b for b in self.bullets if b[0]+4000 < tick]
        for item in dead:
            item[1].expire()
        for b in self.bullets:
            b[1].update()


class Bullet(object):
    def __init__(self, world, spawner, delta):
        self.sprite = retroSnake.Sprite([
            retroSnake.Point(retroSnake.Vector(0, 0))
            ])
        self.sprite.setLocalMatrix(spawner.sprite.getLocalMatrix())
        self.sprite.setWorldMatrix(spawner.sprite.getWorldMatrix())
        self.sprite.applyLocalMatrix(
            retroSnake.newTranslateMatrix(*delta.data[:2])
            )
        self.world = world
        self.spawner = spawner
        world.addSprite(self.sprite)

    def update(self):
        self.sprite.applyLocalMatrix(retroSnake.newTranslateMatrix(0, -8))

    def expire(self):
        self.world.removeSprite(self.sprite)
        self.spawner.bullets.remove(item)


def main():
    if not retroSnake.init():
        print "Error: Could not initialise retroSnake."
        raise SystemExit
    display = retroSnake.setupDisplay(640, 480, "Asteroids")

    world = retroSnake.World()
    camera = retroSnake.Camera(world)
    camera.applyMatrix(retroSnake.newTranslateMatrix(320, 240))

    updater = {}
    handler = {}

    ship = updater["ship"] = handler["ship"] = Ship(world)

    clock = pygame.time.Clock()

    while True:
        pygame.display.set_caption("FPS: %d" % (clock.get_fps(),))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                camera.applyMatrix(retroSnake.newScaleMatrix(2))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                camera.applyMatrix(retroSnake.newScaleMatrix(.5))

            for k in handler.keys():
                updater[k].handle(event)

        for k in updater.keys():
            updater[k].update()

        display.fill((0, 0, 0))
        camera.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
