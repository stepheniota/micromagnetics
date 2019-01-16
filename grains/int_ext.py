## Code produces gaussian distribution interregion exchange
## for use in mumax code
## Stephen Iota
## last updated: Jan 19

import os
import numpy as np

print("Enter mean: ")
mean = input()

print("Enter std: ")
std = input()

print("Enter num of exchanges: ")
length = input()


## generate normal distribution
exchanges = np.random.normal(loc=mean,scale=std,size=length)
print(exchanges)

## create/edit txt file with 
file = open("int_ext.txt","w")
for i in exchanges:
    print("Enter index a: ")
    a = input()
    print("Enter index b: ")
    b = input()
    my_string = "ext_scaleExchange(" + str(a) + "," + str(b) + "," + str(exchanges[i]) + ")\n" 
    file.write(my_string)
file.close() 
