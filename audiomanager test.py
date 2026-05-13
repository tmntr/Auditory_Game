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
        self.itinary