import pygame
import math
import time

pygame.mixer.init()

# Create Sound and Channel instances.
sound0 = pygame.mixer.Sound('pianoc.wav')
channel0 = pygame.mixer.Channel(0)

# Play the sound (that will reset the volume to the default).
#channel0.play(sound0)
# Now change the volume of the specific speakers.
# The first argument is the volume of the left speaker and
# the second argument is the volume of the right speaker.

theta = 0

soundpos = [0,2]

class thing:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def dist(self,ot):
        dx = self.x - ot.x
        dy = self.y - ot.y
        d = (dx**2 + dy**2)**0.5
        return d

le = thing(-0.25,0)
re = thing(0.25,0)

sounder = thing(-4,4)

while True:
    levol = 1/le.dist(sounder)
    revol = 1/le.dist(sounder)
    ratio = levol/revol
    if ratio <= 1:
        channel0.set_volume(ratio,1)
    else:
        channel0.set_volume(1,1/ratio)
    channel0.play(sound0)
    sounder.x+=0.4
    print(sounder.x)
    time.sleep(1)

'''pygame.mixer.music.load('pianoc.wav')
pygame.mixer.music.play(0)'''

#playsound.playsound('pianoc.wav')
