import pygame
import random
import math
import time

from spacing import Physical,PhysHead

REALWIDTH = 20
REALHEIGHT = 15

MULTIPLIER = 40

SCREENWIDTH = REALWIDTH*MULTIPLIER
SCREENHEIGHT = REALHEIGHT*MULTIPLIER

theScreen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

class GameObject:
    def __init__(self,phys,colour = None):
        self.phys = phys
        if colour is None:
            self.colour = random.choice(['red','blue','green','yellow','magenta','cyan'])
        else:
            self.colour = colour

    def draw(self,screen):
        #this drawing method puts 0,0 in the centre of the screen
        apx = self.phys.x+REALWIDTH/2
        apy = -1*self.phys.y+REALHEIGHT/2
        pygame.draw.circle(screen,self.colour,(apx*MULTIPLIER,apy*MULTIPLIER),2)

class Player(GameObject):
    def __init__(self,phys,colour = None,d=0):
        super().__init__(phys,colour)
        self.phys.direction = d
        self.speed = 0.5
        self.rspeed = 0.5
        self.interactlastframe = False

    def control(self,keys,dtime):
        if keys[pygame.K_LEFT]:
            self.phys.direction -= 2*math.pi*dtime*self.rspeed
        if keys[pygame.K_RIGHT]:
            self.phys.direction += 2*math.pi*dtime*self.rspeed
        if keys[pygame.K_UP]:
            self.phys.movepolar(self.speed*dtime,0)
        if keys[pygame.K_DOWN]:
            self.phys.movepolar(-1*self.speed*dtime,0)

        if keys[pygame.K_SPACE]:
            if not self.interactlastframe:
                self.switch()
            self.interactlastframe = True
        else:
            self.interactlastframe = False

    def draw(self,screen):
        apx = self.phys.x + REALWIDTH / 2
        apy = -1 * self.phys.y + REALHEIGHT / 2
        apx2 = apx + 0.5*math.sin(self.phys.direction)
        apy2 = apy - 0.5*math.cos(self.phys.direction)
        pygame.draw.line(screen, "black", (apx * MULTIPLIER, apy * MULTIPLIER), (apx2 * MULTIPLIER, apy2 * MULTIPLIER), 1)
        pygame.draw.circle(screen, self.colour, (apx * MULTIPLIER, apy * MULTIPLIER), 3)

    def validswitch(self,switch):
        '''

        Parameters
        ----------
        switch: the switch object who is being tested to see whether it is acceptable to

        Returns
        -------
        a boolean value determining whether this switch is in a good place to be used
        '''
        bearing = self.phys.get_relative_bearing(switch.phys)
        distance = self.phys.dist(switch.phys)
        if (bearing < 0.5 or bearing > 2*math.pi-0.5) and distance < 0.5:
            return True
        else:
            return False


class Switch(GameObject):
    def __init__(self,phys,startstate = False):
        if startstate:
            colour = "cyan"
        else:
            colour = "red"
        super().__init__(phys,colour)
        self.state = startstate

    def switch(self):
        if self.state:
            self.state = False
            self.colour = "red"
        else:
            self.state = True
            self.colour = "cyan"






monophys = Physical(0,0)
Monolith = Switch(monophys)

deckphys = Physical(0,0)
Deckard = Player(deckphys,"red")

time0 = 0
time1 = time.time()
while True:
    time1 = time.time()
    deltatime = time1-time0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    keys = pygame.key.get_pressed()


    theScreen.fill((255,255,255))
    Monolith.draw(theScreen)
    if Deckard.validswitch(Monolith):
        Monolith.switch()
    Deckard.draw(theScreen)
    Deckard.control(keys,deltatime)
    pygame.display.flip()
    time0 = time1





pygame.init()