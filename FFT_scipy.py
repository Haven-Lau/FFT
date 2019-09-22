import matplotlib.pyplot as plt

import pydub
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np

seg1 = pydub.AudioSegment.from_file('Noise.m4a', 'm4a')
seg2 = pydub.AudioSegment.from_file('Voice w noise.m4a', 'm4a')
# plotting
fig, axarr = plt.subplots(3, 2)
fft_old = 0
for i, seg in enumerate([seg1, seg2]):
    print("Information:")
    print("Channels:", seg.channels)
    print("Bits per sample:", seg.sample_width * 8)
    print("Sampling frequency:", seg.frame_rate)
    print("Length:", seg.duration_seconds, "seconds")

    samples = np.array(seg.get_array_of_samples())
    axarr[0, i].plot(samples)

    Fs = 44100
    N = samples.shape[0]

    # fourier transform and frequency domain
    #
    Y_k = np.fft.fft(samples)[0:int(N/2)]/N  # FFT function from numpy
    Y_k[1:] = 2*Y_k[1:]  # need to take the single-sided spectrum only
    Pxx = np.abs(Y_k)  # be sure to get rid of imaginary part
    Pxx[Pxx < 0.001] = 0

    f = Fs*np.arange((N/2))/N  # frequency vector

    axarr[1, i].plot(f, Pxx, linewidth=2)
    axarr[1, i].set_xscale('log')
    axarr[1, i].set_yscale('log')
    # axarr[2, i].plot(f, Pxx - fft_old, linewidth=2)
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency [Hz]')
    fft_old = Pxx


plt.show()
