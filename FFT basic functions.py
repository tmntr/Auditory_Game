import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import random


p = pyaudio.PyAudio()

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

magnitude = np.abs(fft_values)



new_sample = np.fft.ifft(fft_values)



for i in range(len(freq)//2):
    print(f"{freq[i]:.2f} Hz, {magnitude[i]:.2f}")



def alterValueByDecibels(value, decibels):
    return value*10**(decibels/10)


#for i in range(len(freq)//2):
#    if 2000 < freq[i] < 5000:
#  magnitude[i] = alterValueByDecibels(magnitude[i], 17)






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








