import retroSnake
from retroSnake import pygame


def main():
    if not retroSnake.init():
        print "Error: Could not initialise retroSnake."
        raise SystemExit
    display = retroSnake.setupDisplay(640, 480, "Asteroids")

    world = retroSnake.World()
    camera = retroSnake.Camera(world)
    camera.applyMatrix(retroSnake.newTranslateMatrix(320, 240))

    line = retroSnake.Sprite([retroSnake.Line(
        retroSnake.Vector(-20, -20),
        retroSnake.Vector(20, 20))])
    box = retroSnake.Sprite([
        retroSnake.LineLoop(
            retroSnake.Vector(-20, -20),
            retroSnake.Vector(20, -20),
            retroSnake.Vector(20, 20),
            retroSnake.Vector(-20, 20),
            )
        ])
    world.addSprite(line)
    world.addSprite(box)

    clock = pygame.time.Clock()

    while True:
        pygame.display.set_caption("FPS: %d" % (clock.get_fps(),))
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                camera.applyMatrix(retroSnake.newScaleMatrix(2))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                camera.applyMatrix(retroSnake.newScaleMatrix(.5))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            line.applyWorldMatrix(retroSnake.newTranslateMatrix(5, 0))
        if keys[pygame.K_LEFT]:
            line.applyWorldMatrix(retroSnake.newTranslateMatrix(-5, 0))
        if keys[pygame.K_UP]:
            line.applyWorldMatrix(retroSnake.newTranslateMatrix(0, -5))
        if keys[pygame.K_DOWN]:
            line.applyWorldMatrix(retroSnake.newTranslateMatrix(0, 5))

        if keys[pygame.K_d]:
            box.applyWorldMatrix(retroSnake.newTranslateMatrix(5, 0))
        if keys[pygame.K_a]:
            box.applyWorldMatrix(retroSnake.newTranslateMatrix(-5, 0))
        if keys[pygame.K_w]:
            box.applyWorldMatrix(retroSnake.newTranslateMatrix(0, -5))
        if keys[pygame.K_s]:
            box.applyWorldMatrix(retroSnake.newTranslateMatrix(0, 5))

        box.applyLocalMatrix(retroSnake.newRotateMatrix(.01))
        line.applyLocalMatrix(retroSnake.newRotateMatrix(-.01))

        display.fill((0, 0, 0))
        camera.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
