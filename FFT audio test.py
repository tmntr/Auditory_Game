import pyaudio
from scipy.fft import fft, ifft
from wavio import read
import numpy

p = pyaudio.PyAudio()


'''def boostFrequ(frames, index, amount):
    frequs = fft(frames, 8)
    print(frequs)
    frequs[index] *= complex(amount)
    return ifft(frequs)


class SingleSoundManager:
    def __init__(self,samplerate):
        self.samplerate = samplerate
        self.stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=samplerate,
                    output=True)
        self.frameslength = samplerate * 4
        self.frames = []
        self.index = 0
    def update(self):
        outputbytes = numpy.array(self.frames,'float32').tobytes()
        self.stream.write(outputbytes)
    def addsound(self,array):
        self.frames = array

class Soundemitter:
    def __init__(self,soundfile,manager):
        self.soundfile = soundfile
        self.sound = []
        self.converttoarray()
        self.index = 0
        self.manager = manager
        self.volume = 1
        self.framelength = 1000
    def converttoarray(self):
        filedata = read(self.soundfile).data.tolist()
        if len(filedata[0]) == 1:
            sound = [item[0] for item in filedata]
        else:# len(filedata[0]) == 2:
            sound = [item[1] for item in filedata]

        #any sound files entered in will automatically adjust themselves so that no frame > 1
        loudest = max(sound)
        for i in range(0, len(sound)):
            sound[i] /= loudest*10
        self.sound = sound

    def boost(self,frames,amount):
        frequs = fft(frames,8)
        for index in range(4,5):
            frequs[index] *= complex(amount)
        return ifft(frequs)


    def writeSound(self):
        self.manager.addsound(self.boost(self.sound[self.index:min(len(self.sound),self.framelength+self.index)],10))
        self.index += self.framelength

manager = SingleSoundManager(44100)

piano = Soundemitter(soundfile="pianoc.wav",manager=manager)


while piano.index < len(piano.sound):
    piano.writeSound()

manager.update()'''