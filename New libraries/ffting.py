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
        newsignal[i] = fftedsignal[i] * (physicsing.quick_attenuate(fftedsignal[i],sf))

    new_sample = np.real(np.fft.ifft(newsignal, N, norm='forward'))

    return new_sample