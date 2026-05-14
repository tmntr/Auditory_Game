import numpy
import pyaudio

p = pyaudio.PyAudio()

class Manager:
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
        self.stream.write(current_frame)
        self.frames[self.index] = 0
        self.index = (self.index + 1) % self.frameslength
    def addsound(self,value):
        self.frames[self.index] += value

class Soundemitter:
    def __init__(self,samplerate,soundfile):
        self.samplerate = samplerate
        self.sound = []

while True:
