import pygame
import time

numberofwobbles = 2

SCREENWIDTH = 1600
SCREENHEIGHT = 900

MAXAGE = 1
MAXDISTANCE = 1
z0 = 0.5
pygame.init()

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

class Wobble:
    def __init__(self,screen,forward,right):
        self.border=5
        self.screen = screen
        self.forward = forward
        self.right = right
        self.width = SCREENWIDTH
        self.height = SCREENHEIGHT
        self.age = 0
        self.x = 0
        self.y = 0
        self.initialstrength = 1
        self.z = 0
        if self.forward < 0:
            self.z = MAXDISTANCE

    def distance(self):
        if self.forward > 0:
            return (self.x**2+self.y**2+self.z**2)**0.5
        else:
            return (self.x**2+self.y**2+(MAXDISTANCE-self.z**2))**0.5
    def cycle(self,time=0):
        self.age += time
        self.x += self.right*time
        self.z += self.forward*time
        self.width = SCREENWIDTH*z0/(z0+self.z)
        self.height = SCREENHEIGHT*z0/(z0+self.z)

        #self.width = SCREENWIDTH*(1/2**(self.z))
        #self.height = SCREENHEIGHT*(1/2**(self.z))

    def display(self):

        colour = int(255*self.initialstrength*(1-self.distance()/MAXDISTANCE))

        apparentx = self.x*340*z0/(z0+self.z)

        pygame.draw.rect(self.screen,(colour,colour,colour),pygame.Rect(apparentx-self.width/2+SCREENWIDTH/2,self.y-self.height/2+SCREENHEIGHT/2,self.width,self.height),self.border)



forward = 0.125
right = 1

wobbles = [Wobble(screen,forward,right)]

time0 = 0
time1 = time.time()
while True:
    #thinking
    time0 = time.time()
    deltatime = time0 - time1
    wobblekilllist = []
    for wobble in wobbles:
        wobble.cycle(deltatime)
        if wobble.distance() > MAXDISTANCE:
            wobblekilllist.append(wobble)
    time1 = time0
    if not len(wobbles):
        wobbles.append(Wobble(screen, forward, right))
    else:
        if len(wobbles) < numberofwobbles:
            if wobbles[-1].distance() > MAXDISTANCE / numberofwobbles:
                wobbles.append(Wobble(screen, forward, right))
    for item in wobblekilllist:
        wobbles.remove(item)
    if deltatime >= 0:
        #showing
        screen.fill(0)
        for wobble in wobbles:
            wobble.display()
        pygame.display.flip()