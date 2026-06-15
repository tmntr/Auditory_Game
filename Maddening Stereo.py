import numpy
import pyaudio
import math
from wavio import read
import array

p = pyaudio.PyAudio()

class StereoManager:
    def __init__(self,samplerate):
        self.samplerate = samplerate
        self.stream = p.open(format=pyaudio.paFloat32,
                             channels=2,
                             rate=samplerate,
                             output=True)
        self.frameslength = samplerate * 5
        self.framesl = numpy.array([0.0 for x in range(0, self.frameslength)])
        self.framesr = numpy.array([0.0 for x in range(0, self.frameslength)])
        self.index = 0
    def addsound(self,valuel,valuer,offsetl = 0,offsetr = 0):
        self.framesl[(self.index+offsetl)%self.frameslength] += valuel
        self.framesr[(self.index + offsetr) % self.frameslength] += valuer
    def update(self):
        currentl = self.framesl[self.index]
        currentr = self.framesr[self.index]
        both = [currentl,currentr]
        outputbytes = numpy.array(both,'float32').tobytes()#
        self.stream.write(outputbytes)
        self.framesl[self.index] = 0
        self.framesr[self.index] = 0



class StereoSoundemitter:
    def __init__(self,soundfile,manager):
        self.soundfile = soundfile
        self.sound = numpy.ndarray([])
        self.converttoarray()
        self.index = 0
        self.manager = manager
        self.volume = 0.00390625/2
        self.volumel = self.volume
        self.volumer = self.volume
    def converttoarray(self):
        filedata = numpy.array((read(self.soundfile).data).tolist(),dtype=float)
        if len(filedata[0]) == 1:
            sound = numpy.array([item[0] for item in filedata])
        else:# len(filedata[0]) == 2:
            sound = numpy.array([item[1] for item in filedata])

        #any sound files entered in will automatically adjust themselves so that no frame > 1
        loudest = sound.max()
        for i in range(0, len(sound)):
            sound[i] /= loudest/64
        self.sound = sound
    def update(self):
        current_frame = self.sound[self.index]
        self.manager.addsound(current_frame*self.volumel,current_frame*self.volumer)
        self.index += 1
        self.index %= len(self.sound)

manager = StereoManager(44100)

annoyingpiano = StereoSoundemitter(soundfile="pianoc.wav",manager=manager)

while True:
    annoyingpiano.update()
    manager.update()