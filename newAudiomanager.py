import numpy as np
import pyaudio
from wavio import read
import time

p = pyaudio.PyAudio()

class AudioManager:
    def __init__(self,channels = 2, samplerate = 44100):
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
    def __init__(self):
        self.sound = np.array([])
        self.tempsound = self.sound
        self.index = 0
        self.playing = False

    def sendFrame(self,value):
        self.sound = np.append(self.sound,value)


'''myHeart = AudioManager()

running = True

t = 0
frequency = 440

while t < 4:
    t += 1/44100
    value = 0.5*np.sin(2*np.pi*frequency*t)
    valuel = value
    valuer = value

    myHeart.queueSoundFrame(value,valuer)
    myHeart.cycle()'''