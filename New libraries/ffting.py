import numpy as np
import math



def attenuate_sample(sample,sf,Fs = 44100):
    T = 1 / Fs
    N = len(sample)
    fftedsignal = np.fft.fft(sample, N, norm='forward')
    # print(fftedsignal)
    newsignal = np.zeros(N, dtype=np.complex128)
    freq = np.fft.fftfreq(N, T)
    for i in range(len(fftedsignal)):
        newsignal[i] = fftedsignal[i] * (sf)**(freq[i]**2)

    new_sample = np.real(np.fft.ifft(newsignal, N, norm='forward'))

    return new_sample