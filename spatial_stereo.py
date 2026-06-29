from maddening_stereo import *
from sound_profiler import *
import time

class Head:
    def __init__(self,body,samplerate=44100):
        self.earl = Ear(-0.175,0)
        self.earr = Ear(0.175,0)

        self.manager = StereoManager(samplerate=samplerate)
        self.body = body
        self.updatepos()
        self.angle = 0
    def update(self):
        self.manager.update()
    def updatepos(self):
        self.earl.x,self.earl.y = self.body.x+0.175*math.cos(self.body.angle), self.body.y+0.175*math.sin(self.body.angle)
        self.earr.x,self.earr.y = self.body.x-0.175*math.cos(self.body.angle), self.body.y-0.175*math.sin(self.body.angle)

class Noise:
    def __init__(self,x,y,sound,manager):
        self.body = Emitter(x,y)
        self.voice = StereoSoundemitter(sound,manager)
    def update(self,profile):
        self.voice.update(profile)

'''left = Ear(-0.175,0)
right = Ear(0.175,0)
head = Head(left,right)

piano = Noise(-5,0,"pianoc.wav",head.manager)
t = time.time()
while True:
    deltatime = time.time() - t
    t = time.time()
    profilel = head.earl.sound_profile(piano.body)
    profiler = head.earr.sound_profile(piano.body)

    piano.update((profilel,profiler))
    head.update()
    head.updatepos()'''
