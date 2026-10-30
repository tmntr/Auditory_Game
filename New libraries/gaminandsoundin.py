import pygame
import time
import random
import threading

from spacing import Physical,PhysHead
from gaming import Player,Switch,screensettings
from sounding import Head,AudioManager,Sounder

#this class wraps the audio and game capabilities of the player into one
class User:
    def __init__(self,name):
        self.name = name
        self.phys = Physical(0,0,0.05,0)
        self.left = Physical(-0.1,0,0.05,0)
        self.right = Physical(0.1,0,0.05,0)


        myphyshead = PhysHead(self.phys,self.left,self.right,0)

        self.head = Head(myphyshead,AudioManager())
        self.player = Player(self.head.physhead.centre)
class AudioSwitch:
    def __init__(self,phys):
        self.phys = phys
        self.sounder = Sounder(self.phys)
        self.gameObject = Switch(self.phys)



class Game:
    def __init__(self,user):
        self.user = user
        self.sounders = []
        self.running = True


    def update(self,keys,deltatime):

        self.user.player.control(keys,deltatime)
        self.user.player.update(self.sounders)


#        print(self.user.player.phys.y)

    def addSwitch(self,x,y,startState,soundstate):
        phys = Physical(x,y,0.3,0)
        switch = AudioSwitch(phys)
        switch.sounder.set_sound_as_file(soundstate)
        switch.gameObject.state = startState
        self.sounders.append(switch)




    def draw(self,screen):

        screen.fill((255, 255, 255))
        self.user.player.draw(screen)

        for thing in self.sounders:
            thing.gameObject.draw(screen)

        # pygame.display.flip()

    def sound(self):
        for thing in self.sounders:
            thing.sounder.cycle(self.user.head)
        self.user.head.listen()





pygame.init()

myScreen = pygame.display.set_mode(screensettings)

flynn = User("Flynn")

theGame = Game(flynn)

theGame.addSwitch(0.1,0,True,'nestednicewaves.wav')

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






