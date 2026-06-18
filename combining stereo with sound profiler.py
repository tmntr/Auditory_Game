from maddening_stereo import *
from sound_profiler import *

class Head:
    def __init__(self,earl,earr,samplerate=44100):
        self.earl = earl
        self.earr = earr
        self.manager = StereoManager(samplerate=samplerate)
    def update(self):
        self.manager.update()

class Noise:
    def __init__(self,x,y,sound,manager):
        self.body = Emitter(x,y)
        self.voice = StereoSoundemitter(sound,manager)
    def update(self,profile):
        self.voice.update(profile)

left = Ear(-0.175,0)
right = Ear(0.175,0)
head = Head(left,right)

piano = Noise(10,2,"pianoc.wav",head.manager)

while True:
    profilel = head.earl.sound_profile(piano.body)
    profiler = head.earr.sound_profile(piano.body)

    piano.update((profilel,profiler))
    head.update()
    piano.body.x-=0.0001