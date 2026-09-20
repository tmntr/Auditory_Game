import numpy as np
import matplotlib.pyplot as plt
import pyaudio
from wavio import read

import random
import time


def alterValueByDecibels(value, decibels):
    return value*10**(decibels/10)



Fs = 44100
T = 1/Fs

'''t = np.arange(0, 1, T)
signal = 0*t



for i in range(10):
    signal = signal + 0.0001 * np.sin(2*np.pi*random.randint(1,44100//8)*t)
fft_values = np.fft.fft(signal)'''

soundfile = 'nicewaves.wav'

ogsignal = (read(soundfile).data).tolist()
signal = np.zeros(len(ogsignal))
print(ogsignal[0])
for i in range(len(ogsignal)):
    signal[i] = ogsignal[i][0]

greatestamplitude = max(signal)
signal = signal/greatestamplitude/100

print(signal[0] for item in signal)
print(ogsignal[0] for item in ogsignal)

N = len(signal)


print("Generated")



'''new_fft_values = fft_values


magnitude = np.abs(fft_values)'''

#print(new_fft_values)

def boostfreq(sample, lowerbound, upperbound, amount, Fs = 44100):
    T = 1/Fs
    N = len(sample)
    fftedsignal = np.fft.fft(sample,N,norm='forward')
    #print(fftedsignal)
    newsignal = np.zeros(N,dtype=np.complex128)
    freq = np.fft.fftfreq(N, T)
    for i in range(len(fftedsignal)):

        if lowerbound <= freq[i] <= upperbound:

            #newreal = alterValueByDecibels(fftedsignal[i].real, amount)
            #newimaginary = fftedsignal[i].imag
            #newsignal[i] = newreal + newimaginary * 1.0j
            #newsignal[i] += alterValueByDecibels(fftedsignal[i].real, amount)
            #newsignal[i] += alterValueByDecibels(fftedsignal[i].imag, amount)*1.0j
            newsignal[i] += alterValueByDecibels(fftedsignal[i], amount)

        else:
            newsignal[i] = fftedsignal[i]

    new_sample = np.real(np.fft.ifft(newsignal,N,norm='forward'))

    return new_sample

def triangleboostfreq(sample, lowerbound, upperbound, primaryres, amount, Fs = 44100):
    T = 1 / Fs
    N = len(sample)
    fftedsignal = np.fft.fft(sample, N, norm='forward')
    # print(fftedsignal)
    newsignal = np.zeros(N, dtype=np.complex128)
    freq = np.fft.fftfreq(N, T)
    for i in range(len(fftedsignal)):

        if lowerbound <= freq[i] <= upperbound:

            # newreal = alterValueByDecibels(fftedsignal[i].real, amount)
            # newimaginary = fftedsignal[i].imag
            # newsignal[i] = newreal + newimaginary * 1.0j
            frequency = freq[i]
            if frequency < primaryres:
                individualamount = amount * (frequency-lowerbound)/(primaryres-lowerbound)

            else:
                individualamount = amount * (upperbound-frequency)/(upperbound-primaryres)
            print(f"{frequency} -> {individualamount}")
            newsignal[i] += alterValueByDecibels(fftedsignal[i],individualamount)

        else:
            newsignal[i] = fftedsignal[i]

    new_sample = np.real(np.fft.ifft(newsignal, N, norm='forward'))

    return new_sample


t = np.arange(0, 1, T)

sinesignal = np.sin(2*np.pi*random.randint(1,44100//8)*t)



new_signal = boostfreq(sinesignal, 2000, 5000, 17)





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

plt.subplot(2, 1, 2)
plt.plot(t, new_signal)
plt.title('Time Domain Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.show()'''


p = pyaudio.PyAudio()


stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=Fs,
                output=True,)


f1 = 2000
f2 = 5000

print("Playing")
done = False
index = 0
blocksize = 4410*2
while not done:
    if index+blocksize > N:
        lastindex = N
    else:
        lastindex = index+blocksize

    currentblock = signal[index:lastindex]

    boosted = triangleboostfreq(currentblock,f1,f2,2700,17)

    miniindex = 0
    while miniindex < len(boosted):
        stream.write(np.array([boosted[miniindex]]).astype(np.float32).tobytes())
        miniindex += 1
    index += blocksize
    if index > N:
        done = True


