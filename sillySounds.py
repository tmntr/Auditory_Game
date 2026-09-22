import numpy as np
import pyaudio

p = pyaudio.PyAudio()

sr = 44100

T = 10

signal = np.zeros(T*sr)

frequency = 440


for i in range(len(signal)):
    signal[i] = np.sin(2*np.pi*i/sr * (frequency ** -(np.sin(0.5**5*(frequency) * i / sr * 2*np.pi))))



stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sr,
                output=True,)
stream.write(np.array(signal).astype(np.float32).tobytes())