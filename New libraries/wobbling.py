import pygame
import time

numberofwobbles = 10

SCREENWIDTH = 1600
SCREENHEIGHT = 900

MAXAGE = 4
MAXDISTANCE = 10

pygame.init()

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

class Wobble:
    def __init__(self,screen,forward,right):
        self.screen = screen
        self.forward = forward
        self.right = right
        self.width = SCREENWIDTH
        self.height = SCREENHEIGHT+20
        self.age = 0
        self.x = SCREENWIDTH/2
        self.y = SCREENHEIGHT/2
        self.z = 0

    def cycle(self,time=0):
        self.age += time
        self.x += self.right*time*340
        self.z += self.forward*time
        self.width = SCREENWIDTH*(1/2**(self.z))
        #self.height = SCREENHEIGHT*(1/2**(self.z))


    def display(self):
        colour = int(255*(1-self.age/MAXAGE))

        pygame.draw.rect(self.screen,(colour,colour,colour),pygame.Rect(self.x-self.width/2,self.y-self.height/2,self.width,self.height),5)



forward = 1
right = 0

wobbles = [Wobble(screen,forward,right)]

time0 = 0
time1 = time.time()
while True:
    time0 = time.time()
    deltatime = time0 - time1
    screen.fill(0)
    wobblekilllist = []
    for wobble in wobbles:
        wobble.display()
        wobble.cycle(deltatime)
        if wobble.age > MAXAGE:
            wobblekilllist.append(wobble)
    if len(wobbles) < numberofwobbles:
        if wobbles[-1].age > MAXAGE / numberofwobbles:
            wobbles.append(Wobble(screen, forward, right))
    for item in wobblekilllist:
        wobbles.remove(item)
    pygame.display.flip()
    time1 = time0