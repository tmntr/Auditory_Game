import numpy
import pyaudio
from wavio import read
import array

p = pyaudio.PyAudio()



class MonoManager:
    def __init__(self,samplerate):
        self.samplerate = samplerate
        self.stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=samplerate,
                    output=True)
        self.frameslength = samplerate * 4
        self.frames = [0 for x in range(0, self.frameslength)]
        self.index = 0
    def update(self):
        current_frame = self.frames[self.index]
        output_bytes = array.array('f', [current_frame]).tobytes()
        self.stream.write(output_bytes)
        self.frames[self.index] = 0
        self.index = (self.index + 1) % self.frameslength
    def addsound(self,value):
        self.frames[self.index] += value

class Soundemitter:
    def __init__(self,soundfile,manager):
        self.soundfile = soundfile
        self.sound = []
        self.converttoarray()
        self.index = 0
        self.manager = manager
        self.volume = 1
    def converttoarray(self):
        filedata = (read(self.soundfile).data).tolist()
        if len(filedata[0]) == 1:
            sound = [item[0] for item in filedata]
        else:# len(filedata[0]) == 2:
            sound = [item[1] for item in filedata]

        #any sound files entered in will automatically adjust themselves so that no frame > 1
        loudest = max(sound)
        for i in range(0, len(sound)):
            sound[i] /= loudest
        self.sound = sound
    def update(self):
        current_frame = self.sound[self.index]
        self.manager.addsound(current_frame*self.volume)
        self.index += 1
        self.index %= len(self.sound)

manager = MonoManager(44100)

annoyingpiano = Soundemitter(soundfile="pianoc.wav",manager=manager)

#backgroundnoise = Soundemitter(soundfile="Unfiltered_ambience.wav",manager=manager)
#print("Ambience done")
'''ingenuity = Soundemitter(soundfile="ingenuity.wav",manager=manager)
print("Ingenuity done")
laser = Soundemitter(soundfile="Perseverance_laser.wav",manager=manager)
print("Laser done")
dust_removal = Soundemitter(soundfile="Filtered_gaseous_dust_removal.wav",manager=manager)
print("Dust removal done")
driving = Soundemitter(soundfile="Perseverance_driving.wav",manager=manager)
print("Driving done")


#backgroundnoise.volume = 0.5
ingenuity.volume = 0.25
laser.volume = 0.125
dust_removal.volume = 0.25
driving.volume = 0.25'''

annoyingpiano.volume = 0.03125/8

while True:
    annoyingpiano.update()
    #backgroundnoise.update()
    '''ingenuity.update()
    laser.update()
    dust_removal.update()
    driving.update()'''
    manager.update()
    #In theory, so long as game processing is very light, it can be done in the same loop as the audio processing.
    #If it is too heavy, it will affect the sound adversely. NO PRINTING STUFF
