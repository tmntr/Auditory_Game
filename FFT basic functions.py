import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import random


def alterValueByDecibels(value, decibels):
    return value*10**(decibels/10)

#p = pyaudio.PyAudio()
Fs = 441000
T = 1/Fs

t = np.arange(0, 1, T)
f1 = 50
signal = 0.7*np.sin(2*np.pi*f1*t)



for i in range(15):
    signal = signal + random.random() * np.sin(2*np.pi*random.randint(1,10000)*t)
fft_values = np.fft.fft(signal)

N = len(signal)

freq = np.fft.fftfreq(N, T)




new_fft_values = fft_values


magnitude = np.abs(fft_values)

for i in range(len(freq)//2):
    if 2000 < freq[i] < 5000:
        newreal = alterValueByDecibels(new_fft_values[i].real, 17)
        newimaginary = new_fft_values[i].imag
        new_fft_values[i] = newreal + newimaginary * 1.0j

new_sample = np.abs(np.fft.ifft(new_fft_values))
print(signal)




print(new_sample)









'''plt.subplot(2, 1, 1)
plt.plot(t, signal)
plt.title('Time Domain Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(2, 1, 1)
plt.stem(freq[:N//2], magnitude[:N//2])
plt.title('Frequency Domain (Magnitude Spectrum)')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.tight_layout()



plt.subplot(2, 1, 2)
plt.stem(freq[:N // 2], magnitude[:N // 2])
plt.title('Frequency Domain (Magnitude Spectrum)')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.tight_layout()

plt.show()'''








