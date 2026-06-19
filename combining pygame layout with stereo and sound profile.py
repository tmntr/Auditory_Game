from pygame_layout import *
from spatial_stereo import *



mc = Player(100, 100, 'cyan')

things = [InteractObject(200, 200,'pianoc.wav',mc)]

while True:
    t = pygame.time.get_ticks()
    # deltaTime in milliseconds.
    deltaTime = (t - getTicksLastFrame)
    getTicksLastFrame = t
    timeelapsed = t / 1000

    for thing in things:
        thing.update()

    if pygame.event.get(pygame.QUIT):
        break
    keys = pygame.key.get_pressed()

    mc.control(keys,things)

    screen.fill("black")
    mc.display()
    for item in things:
        item.display()

    pygame.display.flip()
