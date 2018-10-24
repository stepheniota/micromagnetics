## Generatate a ST-FMR meshplot from mumax3 data
## Stephen Iota
## last updated: 10.24.18
## version: 0.0

import numpy as np
import matplotlib.pyplot as plt

#data_name = input("enter data file name: ")

## for testing purposes
data = np.random.rand(10,100)

print(data.shape)

xx,yy = np.meshgrid(len(data[0]),len(data[1]))

plt.pcolormesh(xx,yy,data)
plt.imshow()

