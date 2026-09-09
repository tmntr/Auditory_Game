import numpy as np
import matplotlib.pyplot as plt
import random

Fs = 44100

t = np.arange(0, 1, 1/Fs)

signal = np.sin(2*np.pi*5*t)

for i in range(10):
    signal = signal + np.sin(2*np.pi*random.randint(1,2000)*t)

plt.figure(figsize = (10,4))

plt.plot(t, signal)
plt.title("Original signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

fft_output = np.fft.fft(signal)

n = len(signal)
freqs = np.fft.fftfreq(n, 1/Fs)

plt.figure(figsize = (10,4))
plt.plot(freqs, np.abs(fft_output))
plt.title("Frequency Spectrum (Magnitude)")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.show()

ifft_output = np.fft.ifft(fft_output)

reconstructed_signal = np.real(ifft_output)

print(signal)
print(reconstructed_signal)

plt.figure(figsize = (10,4))
plt.plot(t,reconstructed_signal)
plt.title("Reconstructed Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()