#!/usr/bin/python3.5

## fft of mumax m_xyz data
## stephen iota

import os
import numpy as np
from scipy import fftpack, signal
import matplotlib.pyplot as plt

## generate test data
## gaussian
data = signal.gaussian(100,7,sym=False)

print(data.shape)
print(data)


fftdata = fftpack.fft(data,n=data.shape[0])

plt.plot(data)
plt.plot(fftdata)
plt.legend()
plt.show()
