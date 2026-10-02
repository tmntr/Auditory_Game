import numpy as np
import pyaudio
from wavio import read
import math
import time

p = pyaudio.PyAudio()

SR = 44100

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
    def __init__(self):
        self.sound = np.array([])
        self.lsound = np.array([])
        self.rsound = np.array([])
        self.tempsound = self.sound
        self.index = 0
        self.playing = False

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


    def sendFrame(self,manager,delayl=0,delayr=0):
        offsetl = delayl/SR
        offsetr = delayr/SR
        frame = self.sound[self.index]
        manager.queueSoundFrame(frame,offsetl,offsetr)

    def cycle(self,manager):
        self.sendFrame(manager)
        self.index += 1


    def profile(self):
        pass


#PHYSICAL IMPORTANT THINGS
#1: All angles in radians please.
#2: North is +y
#3: East is +x


#Creating a superclass that will allow basic spatial operations and comparisons to be made
class Physical:
    def __init__(self,x,y,d=None):
        self.x = x
        self.y = y
        #will always be positive
        self.direction = d#%2*math.pi

    #Function to find cartesian distance between 2 objects
    def dist(self,op):
        dx = self.x - op.x
        dy = self.y - op.y
        return (dx**2 + dy**2)**0.5

    #N.B. this should ideally only be used with physical objects with directions.
    #Used to
    def get_bearing(self,op):
        dx = op.x - self.x
        dy = op.y - self.y
        return math.atan2(dx,dy)

    #returns the angle bearing of the Other Physical taking the current physical's facing as north
    def get_relative_bearing(self,op):
        theta = 0
        bearing = self.get_bearing(op)
        theta = (bearing-self.direction)%(2*math.pi)
        return theta


    #Works out as a boolean whether another Physical is overall in front of this one
    def is_infront(self,op):
        if math.cos(self.get_relative_bearing(op)) > 0:
            return True
        else:
            return False

    #returns on a scale of -1 to 1 how "in front" the other Physical is: will be useful when ears begin to implement HRTFs
    def how_in_front(self,op):
        return math.cos(self.get_relative_bearing(op))



class Profiler:
    def __init__(self):



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