import numpy as np
import math
import physicsing



def attenuate_sample(sample,sf,Fs = 44100):
    T = 1 / Fs
    N = len(sample)
    fftedsignal = np.fft.fft(sample, N, norm='forward')
    # print(fftedsignal)
    newsignal = np.zeros(N, dtype=np.complex128)
    freq = np.fft.fftfreq(N, T)
    for i in range(len(fftedsignal)):
        newsignal[i] = fftedsignal[i] * (physicsing.quick_attenuate(sf,freq[i]))

    new_sample = np.real(np.fft.ifft(newsignal, N, norm='forward'))

    return new_sample

def alterValueByDecibels(value, decibels):
    return value*10**(decibels/10)


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
            #print(f"{frequency} -> {individualamount}")
            newsignal[i] += alterValueByDecibels(fftedsignal[i],individualamount)

        else:
            newsignal[i] = fftedsignal[i]

    new_sample = np.real(np.fft.ifft(newsignal, N, norm='forward'))

    return new_sample