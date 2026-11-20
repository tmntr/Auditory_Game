import pygame
import time
import random
import threading

from spacing import Physical,PhysHead,RectPhysical
from gaming import Player,Switch,screensettings,Wall,Link,REALWIDTH,REALHEIGHT,MULTIPLIER
from sounding import Head,AudioManager,Sounder

#this class wraps the audio and game capabilities of the player into one
class User:
    def __init__(self,name):
        self.name = name
        self.eardist = 0.1
        self.phys = Physical(0,0, self.eardist,0)

        myphyshead = PhysHead(self.phys,self.eardist)

        self.head = Head(myphyshead,AudioManager())
        self.player = Player(self.head.physhead.centre)
    @property
    def left(self):
        return self.head.physhead.lear
    @property
    def right(self):
        return self.head.physhead.rear


class AudioSwitch:
    def __init__(self,phys):
        self.phys = phys
        self.sounder = Sounder(self.phys)
        self.gameObject = Switch(self.phys)

class AudioWall:
    def __init__(self,rectPhys):
        self.rectPhys = rectPhys
        self.sounder = Sounder(self.rectPhys)
        self.gameObject = Wall(self.rectPhys)

class Disembodied:
    def __init__(self,x,y,soundfile,looping,w0 = 0.3):
        self.phys = Physical(x,y,w0)
        self.sounder = Sounder(self.phys,looping)
        self.sounder.set_sound_as_file(soundfile)






class Game:
    def __init__(self,user):
        self.user = user
        self.sounders = []
        self.disembodiedsounds = []
        self.links = []
        self.running = True


    def update(self,keys,deltatime):
        for item in self.links:
            item.update()

        self.user.player.control(keys,deltatime)
        self.user.player.update(self.sounders)

        killlist = []
        for item in self.disembodiedsounds:
            if item.sounder.done:
                killlist.append(item)
        for item in killlist:
            self.disembodiedsounds.remove(item)


#        print(self.user.player.phys.y)

    def add_switch(self, x, y, startState, soundname):
        phys = Physical(x,y,0.3,0)
        switch = AudioSwitch(phys)
        switch.sounder.set_sound_as_file(soundname)
        switch.gameObject.state = startState
        self.sounders.append(switch)

    def add_wall(self,x,y,w,h,soundname):
        rectPhys = RectPhysical(x,y,w,h,0.5)
        wall = AudioWall(rectPhys)
        wall.sounder.set_sound_as_file(soundname)
        self.sounders.append(wall)

    def plot_point(self,screen,x,y):


        apx = x + REALWIDTH / 2
        apy = -1 * y + REALHEIGHT / 2
        pygame.draw.circle(screen, 'blue', (apx * MULTIPLIER, apy * MULTIPLIER), 1)

    def one_time_play(self,x,y,soundname):
        self.disembodiedsounds.append(Disembodied(x, y, soundname,False))

    def add_disembodied_voice(self,x,y,soundname):
        self.disembodiedsounds.append(Disembodied(x, y, soundname,True))

    def draw(self,screen):

        screen.fill((255, 255, 255))
        self.user.player.draw(screen)
        self.plot_point(screen,self.user.left.x,self.user.left.y)
        self.plot_point(screen,self.user.right.x,self.user.right.y)

        for thing in self.sounders:
            thing.gameObject.draw(screen)


    def sound(self):
        for thing in self.sounders:
            thing.sounder.cycle(self.user.head)
        for thing in self.disembodiedsounds:
            thing.sounder.cycle(self.user.head)
        self.user.head.listen()

    def link(self,index1,index2):
        if index1 < len(self.sounders) and index2 < len(self.sounders):
            newlink = Link(self.sounders[index1].gameObject,self.sounders[index2].gameObject)
            self.links.append(newlink)





pygame.init()

myScreen = pygame.display.set_mode(screensettings)

flynn = User("Flynn")

theGame = Game(flynn)

#theGame.add_switch(0.1, 0, True, 'nestednicewaves.wav')
theGame.add_wall(2,-2,4,9,'nestednicewaves.wav')
theGame.add_switch(-1,1,True,'nestednicewaves.wav')

theGame.link(0,1)
theGame.one_time_play(0,0,"nestedpianoc.wav")

def pygameCycle(game):
    time0 = 0
    time1 = time.time()
    timesincelastdraw = 0
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                pygame.quit()
        time1 = time.time()
        deltatime = time1 - time0


        keys = pygame.key.get_pressed()
        game.update(keys,deltatime)

        time0 = time1

        if keys[pygame.K_ESCAPE]:
            game.running = False
            pygame.quit()

        if timesincelastdraw > 1/40:
            game.draw(myScreen)
            pygame.display.flip()
            timesincelastdraw = 0
        else:
            timesincelastdraw += deltatime



        #pygame.event.pump()
        time.sleep(0.001)


def audioCycle(game):
    while game.running:
        game.sound()

#pygamecycler = threading.Thread(target=pygameCycle,args=(theGame,))
audiocycler = threading.Thread(target=audioCycle,args=(theGame,))

#pygamecycler.start()
audiocycler.start()


pygameCycle(theGame)