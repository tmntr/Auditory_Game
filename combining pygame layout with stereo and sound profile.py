from pygame_layout import *
from spatial_stereo import *



mc = Player(20, 15, 'cyan')

things = [InteractObject(20, 13,'pianoc.wav',mc),InteractObject(20, 17,'nicewaves.wav',mc)]
getTicksLastFrame = 0

#,InteractObject(25,35,'Dust_devil.wav',mc)
a = 0
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


    if a >= 100:
        screen.fill("black")
        mc.display()
        for item in things:
            item.display()

        pygame.display.flip()
        a = 0
    else:
        a += 1