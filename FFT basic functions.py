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



for i in range(10):
    signal = signal + 0.00001 * np.sin(2*np.pi*random.randint(1,44100//8)*t)
fft_values = np.fft.fft(signal)

N = len(signal)


print("Generated")



new_fft_values = fft_values


magnitude = np.abs(fft_values)

#print(new_fft_values)

def boostfreq(sample, lowerbound, upperbound, amount, Fs = 44100):
    T = 1/Fs
    N = len(sample)
    fftedsignal = np.fft.fft(sample,N,norm='forward')
    newsignal = np.zeros(N,dtype=np.complex128)
    freq = np.fft.fftfreq(N, T)
    for i in range(len(fftedsignal)):

        if lowerbound <= freq[i] <= upperbound:

            #newreal = alterValueByDecibels(fftedsignal[i].real, amount)
            #newimaginary = fftedsignal[i].imag
            #newsignal[i] = newreal + newimaginary * 1.0j
            newsignal[i] += alterValueByDecibels(fftedsignal[i].real, amount)
            newsignal[i] += alterValueByDecibels(fftedsignal[i].imag, amount)*1.0j
            print(newsignal[i])
        else:
            newsignal[i] = fftedsignal[i]

    new_sample = np.real(np.fft.ifft(newsignal,N,norm='forward'))

    return new_sample

f1 = 2000
f2 = 5000


new_signal = boostfreq(signal, f1, f2, 17)

print("Boosted")




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

print("Playing")
data = (signal).astype(np.float32).tobytes()
stream.write(data)
print("Played 1")
time.sleep(2)
new_data = (new_signal).astype(np.float32).tobytes()
stream.write(new_data)
print("Played 2")


