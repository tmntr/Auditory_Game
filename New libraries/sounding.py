import numpy as np
import pyaudio
from wavio import read
from spacing import Physical,PhysHead
import physicsing
import ffting
import math
import time

p = pyaudio.PyAudio()

SR = 44100
SOS = 340

class AudioManager:
    def __init__(self,channels = 2, samplerate = SR):
        self.samplerate = samplerate
        self.stream = p.open(format = pyaudio.paFloat32,
                             channels = 2,
                             rate = self.samplerate,
                             output = True,)
        #I see no reason to have sounds take longer than 2 seconds
        self.length = 2 * samplerate

        self._lframes = np.zeros(self.length)
        self._rframes = np.zeros(self.length)
        self._index = 0

    def queueSoundFrame(self,valuel,valuer,offsetl = 0,offsetr = 0):
        #adding sound to left
        lindex = int(self._index + offsetl*self.samplerate) % self.length
        self._lframes[lindex] += valuel
        #adding sound to right
        rindex = int(self._index + offsetr*self.samplerate) % self.length
        self._rframes[rindex] += valuer


    def cycle(self):
        self.playFrame()
        self._index += 1
        self._index %= self.length


    def playFrame(self):
        currentl = self._lframes[self._index]
        currentr = self._rframes[self._index]
        outputbytes = np.array([currentl,currentr], 'float32').tobytes()  #
        self.stream.write(outputbytes)
        self._lframes[self._index] = 0.0
        self._rframes[self._index] = 0.0


class Sounder:
    def __init__(self,phys):
        self.sound = np.array([])
        self.lsound = np.array([])
        self.rsound = np.array([])
        self.tempsound = self.sound
        self.index = 0
        self.playing = True
        self.phys = phys
        self.profiler = Profiler(phys)
        self.updatespeed = SR//20

    def set_sound_as_file(self,filename):

        filedata = (read(filename).data).tolist()
        if len(filedata[0]) == 1:
            sound = [item[0] for item in filedata]
        else:  # len(filedata[0]) == 2:
            sound = [item[1] for item in filedata]

        # any sound files entered in will automatically adjust themselves so that no frame > 1
        loudest = max(sound)
        for i in range(0, len(sound)):
            sound[i] /= loudest
        self.sound = sound
        self.lsound = np.zeros(len(self.sound))
        self.rsound = np.zeros(len(self.sound))


    def sendFrame(self,manager,delayl=0.0,delayr=0.0):
        offsetl = delayl//SR
        offsetr = delayr//SR
        framel = self.lsound[self.index]
        framer = self.rsound[self.index]
        manager.queueSoundFrame(framel,framer,offsetl,offsetr)

    def cycle(self,listener):
        if self.playing:
            self.profile(listener)
            delays = self.finddelays(listener)
            self.sendFrame(listener.manager,*delays)
            self.index += 1
            if self.index >= len(self.sound):
                self.playing = False
        self.index %= len(self.sound)

    def start(self):
        self.playing = True
        self.index = 0

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def finddelays(self,listener):

        if isinstance(listener,(Head)):
            distl = self.phys.dist(listener.physl)
            distr = self.phys.dist(listener.physr)
        elif isinstance(listener,(Ear)):
            distl = self.phys.dist(listener.phys)
            distr = self.phys.dist(listener.phys)

        dell = distl/SOS
        delr = distr/SOS

        return (dell, delr)



    def profile(self,listener):
        if self.index % self.updatespeed  == 0:
            if self.index + self.updatespeed > len(self.sound):
                finalindex = len(self.sound)
            else:
                finalindex = self.index + self.updatespeed
            sample = np.array(self.sound[self.index:finalindex])
            (samplel,sampler) = self.profiler.profile(sample,listener)
            self.lsound[self.index:finalindex] = samplel
            self.rsound[self.index:finalindex] = sampler




class Profiler:
    def __init__(self,phys):
        #phys is the physical object
        self.phys = phys

    def invsquare(self,soundsample,ophys):
        distance = self.phys.dist(ophys)+self.phys.w0+ophys.w0
        scalefactor = (self.phys.w0/distance)**2
        newsample = soundsample*scalefactor
        return newsample

    def attenuateoverdistance(self,soundsample,ophys,substance = 'air'):
        distance = self.phys.dist(ophys)
        atco = physicsing.ac(substance)
        sf = physicsing.attenuate_scale_factor(atco,distance)
        newsample = ffting.attenuate_sample(soundsample,sf)
        return newsample


    def profile(self,sample,listener):
        if isinstance(listener,(Head)):
            samplel = sample
            samplel = self.invsquare(samplel,listener.physl)
            samplel = self.attenuateoverdistance(samplel,listener.physl,'air')
            sampler = sample
            sampler = self.invsquare(sampler,listener.physr)
            sampler = self.attenuateoverdistance(sampler,listener.physr,'air')
        else:
            sample = self.invsquare(sample,listener.phys)
            sample = self.attenuateoverdistance(sample,listener.phys,'air')
            samplel = sample
            sampler = sample
        return (samplel,sampler)


class Ear:
    def __init__(self,phys,manager):
        self.phys = phys
        self.manager = manager
    def listen(self):
        self.manager.cycle()

class Head:
    def __init__(self,physhead,manager):
        self.physhead = physhead
        self.manager = manager
    def listen(self):
        self.manager.cycle()

    @property
    def physl(self):
        return self.physhead.lear

    @property
    def physr(self):
        return self.physhead.rear


def createHead(x,y,earwidth):
    '''

    Parameters
    ----------
    x : float, the x coordinate of the head's centre
    y : float, the y coordinate of the head's centre
    earwidth : float, the distance between the ears

    Returns
    -------
    A fully constructed head object with Physicals representing its centre and two ears as well as a built in AudioManager
    '''
    return Head(PhysHead(Physical(x,y,0,0),Physical(x-earwidth/2,y),Physical(x+earwidth/2,y)),AudioManager())

def createSounder(x,y,soundname,w0=0.3,started=True):
    thing =  Sounder(Physical(x,y,w0))
    thing.set_sound_as_file(soundname)
    return thing

#me = Ear(Physical(0,0),AudioManager())

'''me = Head(PhysHead(Physical(0,0,0.3,0),Physical(-0.15,0),Physical(0.15,0)),AudioManager())

waves = Sounder(Physical(1,0,5))

waves.set_sound_as_file('nestednicewaves.wav')

time0 = 0
time1 = time.time()

while True:
    time0 = time.time()
    deltatime = time0 - time1


    waves.cycle(me)
    me.listen()

    time1 = time0'''