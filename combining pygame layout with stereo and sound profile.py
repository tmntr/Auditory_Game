from pygame_layout import *
from spatial_stereo import *



mc = Player(20, 40, 'cyan')

things = [InteractObject(20, 30,'pianoc.wav',mc)]
getTicksLastFrame = 0

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

    #screen.fill("black")
    #.display()
    #for item in things:
        #item.display()

    #pygame.display.flip()