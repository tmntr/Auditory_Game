import pygame
import math
from spatial_stereo import *

resmultiplier = 0.03125 * 32

screenwidth = 1920 / 2 * resmultiplier
screenheight = 1080 / 2 * resmultiplier
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.init()


def dist(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return (dx ** 2 + dy ** 2) ** 0.5


class Thing:
    def __init__(self, x, y, colour='white'):
        self.x = x
        self.y = y
        self.colour = colour
        self.speed = 0.5

    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x * resmultiplier, self.y * resmultiplier), 8 * resmultiplier,
                           0)

    def pos(self):
        return (self.x, self.y)


class InteractObject(Thing):
    def __init__(self, x, y, sound, player, colour='red'):
        super().__init__(x, y, colour)
        self.player = player
        self.emitter = Noise(self.x,self.y,sound,self.player.head.manager)

    def interact(self):
        if self.colour == 'red':
            self.colour = 'cyan'
        else:
            self.colour = 'red'
    def update(self):
        if self.colour == 'red':
            profilel = self.player.head.earl.sound_profile(self.emitter.body)
            profiler = self.player.head.earr.sound_profile(self.emitter.body)
            self.emitter.update((profilel,profiler))


class Obstacle(Thing):
    def __init__(self, x, y, w, h, colour='white'):
        super().__init__(x, y, colour)

    def blockbox(self):
        pass


class Player(Thing):
    def __init__(self, x, y, colour='white'):
        super().__init__(x, y, colour)
        self.angle = math.pi
        self.head = Head(self)
        self.reach = 0.75
        self.elastframe = False

    def update(self, keys, things,deltaTime):
        if keys[pygame.K_a]:
            self.x += self.speed * math.cos(self.angle)*deltaTime/1000
            self.y -= self.speed * math.sin(self.angle)*deltaTime/1000
        if keys[pygame.K_d]:
            self.x -= self.speed * math.cos(self.angle)*deltaTime/1000
            self.y += self.speed * math.sin(self.angle)*deltaTime/1000
        if keys[pygame.K_w]:
            self.y += self.speed * math.cos(self.angle)*deltaTime/1000
            self.x += self.speed * math.sin(self.angle)*deltaTime/1000
        if keys[pygame.K_s]:
            self.y -= self.speed * math.cos(self.angle)*deltaTime/1000
            self.x -= self.speed * math.sin(self.angle)*deltaTime/1000

        if keys[pygame.K_e]:
            if not self.elastframe:
                self.elastframe = True
                for item in things:
                    self.interact(item)
        else:
            self.elastframe = False

        if keys[pygame.K_LEFT]:
            self.angle += 1 / 4000 * deltaTime
        if keys[pygame.K_RIGHT]:
            self.angle -= 1 / 4000 * deltaTime

        self.head.update()
        self.head.updatepos()

    def display(self):
        super().display()
        pos = (self.x * resmultiplier, self.y * resmultiplier)
        pos2 = ((self.x + math.sin(self.angle) * self.reach) * resmultiplier,
                (self.y + math.cos(self.angle) * self.reach) * resmultiplier)
        pygame.draw.line(screen, 'white', (pos), (pos2), 1)

    def interact(self, other):
        pos = (self.x, self.y)
        pos2 = ((self.x + math.sin(self.angle) * self.reach), (self.y + math.cos(self.angle) * self.reach))
        if dist(other.pos(), pos) < self.reach / 2 or dist(other.pos(), pos2) < self.reach / 2:
            other.interact()


'''mc = Player(100, 100, 'cyan')

things = [InteractObject(200, 200)]

while True:
    t = pygame.time.get_ticks()
    # deltaTime in milliseconds.
    deltaTime = (t - getTicksLastFrame)
    getTicksLastFrame = t
    timeelapsed = t / 1000

    if pygame.event.get(pygame.QUIT):
        break
    keys = pygame.key.get_pressed()

    mc.control()

    screen.fill("black")
    mc.display()
    for item in things:
        item.display()

    pygame.display.flip()
'''