#!/usr/bin/python3.5

import os
import sys
import numpy as np
import time

starttime = time.time()


## perform fft
mumax_command = "mumax3-fft table.txt"
os.system(mumax_command)
time.sleep(30) # wait to ensure fft finishes
data = np.loadtxt('table_fft.txt',skiprows=1, unpack=True)

mag_data = np.zeros([5, data.shape[1]])
x,y = mag_data.shape

## freq
mag_data[0] = data[0]/(1e9)
## mx
for col in np.arange(1, x, 3):
    mag_data[1] += data[col]
## my
for col in range(2, x, 3):
    mag_data[2] += data[col]
## mz
for col in range(3, x, 3):
    mag_data[3] += data[col]
## full mag
for row in range(0, y):
    for col in range(1,x-1):
        mag_data[4,row] += (mag_data[col,row])**2
    mag_data[4,row] = np.sqrt(mag_data[4,row])


## save data
outputfile = open('mag_table.txt','wb')
np.savetxt(outputfile, mag_data.T,delimiter="\t")
outputfile.close()

totaltime = time.time() - starttime
print("Finished! This script took {} seconds.".format(totaltime))


