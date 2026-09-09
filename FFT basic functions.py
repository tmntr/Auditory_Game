import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import random
import time


def alterValueByDecibels(value, decibels):
    return value*10**(decibels/10)


Fs = 44100
T = 1/Fs

t = np.arange(0, 1, T)
signal = 0*t



for i in range(15):
    signal = signal + 0.0001 * random.random() * np.sin(2*np.pi*random.randint(1,10000)*t)
fft_values = np.fft.fft(signal)

N = len(signal)






new_fft_values = fft_values


magnitude = np.abs(fft_values)

#print(new_fft_values)

def boostfreq(sample, lowerbound, upperbound, amount, Fs = 44100):
    T = 1/Fs
    fftedsignal = np.fft.fft(sample)
    N = len(sample)
    newsignal = np.zeros(N)
    freq = np.fft.fftfreq(N, T)
    for i in range(lowerbound,upperbound):
        newreal = alterValueByDecibels(fftedsignal[i].real, amount)
        newimaginary = fftedsignal[i].imag
        newsignal[i] = newreal + newimaginary * 1.0j

    new_sample = np.real(np.fft.ifft(newsignal))

    return new_sample

f1 = 2000
f2 = 5000


new_signal = boostfreq(signal, f1, f2, 17)






plt.subplot(2, 1, 1)
plt.plot(t, signal)
plt.title('Time Domain Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

'''plt.subplot(2, 1, 1)
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
plt.tight_layout()'''

plt.subplot(2, 1, 2)
plt.plot(t, new_signal)
plt.title('Time Domain Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.show()


p = pyaudio.PyAudio()


stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=Fs,
                output=True,)

data = signal.astype(np.float32).tobytes()
stream.write(data)
time.sleep(1)
new_data = new_signal.astype(np.float32).tobytes()
stream.write(new_data)



