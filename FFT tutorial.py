import time

import matplotlib
import numpy as np
import math
import pyaudio
import wave
import pyglet
import array
from matplotlib import pyplot as plt

'''samplerate = 44100
rootnote = 440
framelength = 512

times = np.arange(framelength)
note1 = np.sin(2 * math.pi * rootnote * times/samplerate)
note2 = np.sin(2 * math.pi * rootnote*4 * times/samplerate)*2

amplitudes = (note1 + note2)/2

frequencies = np.fft.rfftfreq(framelength,d=1/samplerate)
freq_amplitudes = np.abs(np.fft.rfft(amplitudes))

plt.plot(frequencies, freq_amplitudes)
plt.show()'''

class Renderer(pyglet.window.Window):
    bands = np.logspace(2,4,num=8)
    frames_per_buffer = 512

    def __init__(self) -> None:
        super().__init__(1200,800)
        self.batch = pyglet.graphics.Batch()
        self.bars = []
        self.labels = []

        bar_width = self.width/len(self.bands)
        xx = 0
        for band in self.bands:
            xx += bar_width* .05
            self.bars.append(pyglet.shapes.Rectangle(xx,0,bar_width*0.9,self.height/2,color=(30,255,125),batch=self.batch))
            self.labels.append(pyglet.text.Label(str(int(band)),x = xx+bar_width/2,y = self.height-20,color=(30,255,125),anchor_x = 'center', batch=self.batch))
            xx += bar_width* .95

    def start(self, file: wave.Wave_read):
        self.frequencies = np.fft.rfftfreq(self.frames_per_buffer,d=1/file.getframerate())

        def callback(in_data, frame_count: int, time_info, status):
            data = file.readframes(frame_count)
            arrayofints = array.array('h',data)
            leftchannel = arrayofints[::2]
            self.freq_amplitudes = np.abs(np.fft.rfft(leftchannel))


            return (data,pyaudio.paContinue)

        p = pyaudio.PyAudio()
        format = p.get_format_from_width(file.getsampwidth())
        stream = p.open(format=format,channels=file.getnchannels(),frames_per_buffer=self.frames_per_buffer,rate = file.getframerate(),output=True,stream_callback=callback)



        last_time = time.perf_counter()
        while True:
            elapsed_time = time.perf_counter() - last_time
            if elapsed_time > 1/60:
                last_time = time.perf_counter()
                self.dispatch_events()
                self.on_update()
                self.on_draw()
                self.flip()

    def on_update(self):
        band_bucket = np.zeros(len(self.bands))
        for index,band in enumerate(self.bands):
            start_freq = self.bands[index]
            end_freq = start_freq * 2
            for freq_index in range(len(self.freq_amplitudes)):
                if start_freq < self.frequencies[freq_index] < end_freq:
                    if self.freq_amplitudes[freq_index] > band_bucket[index]:
                        band_bucket[index] = self.freq_amplitudes[freq_index]
                if band_bucket[index] > self.bars[index].height:
                    self.bars[index].height = band_bucket[index]
                else:
                    self.bars[index].height /= 1.11

    def on_draw(self):
        self.clear()
        self.batch.draw()

with wave.open("Filtered_gaseous_dust_removal.wav", 'rb') as filey:
    print(f'samplewidth: {filey.getsampwidth()} bytes')
    print(f'channels: {filey.getnchannels()}')
    print(f'framerate: {filey.getframerate()} Hz')

    render = Renderer()
    render.start(filey)
