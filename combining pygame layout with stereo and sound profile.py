from pygame_layout import *
from spatial_stereo import *



mc = Player(20, 35, 'cyan')

things = [InteractObject(20, 33,'pianoc.wav',mc),InteractObject(20, 37,'nicewaves.wav',mc)]
getTicksLastFrame = 0

#,InteractObject(25,35,'Dust_devil.wav',mc)

while True:
    t = pygame.time.get_ticks()
    # deltaTime in milliseconds.
    deltaTime = (t - getTicksLastFrame)

    getTicksLastFrame = t
    timeelapsed = t / 1000

    for thing in things:
        thing.update()

    if pygame.event.get(pygame.QUIT):
        print(deltaTime)
        break
    keys = pygame.key.get_pressed()

    mc.update(keys, things,deltaTime)

    screen.fill("black")
    mc.display()
    for item in things:
        item.display()

    pygame.display.flip()