## Autogenerate graining in mumax
## Stephen Iota

import os
import numpy as np

# create/edit script
script = open("mumax-script.txt","w")

## Materials
print("Enter top material: ")
top = input()
print("Enter bottom material: ")
bottom = input()

## Number of grids
print("Enter number of material regions: ")
num_regions = int(input())
print(num_regions)

## Create region names
region_names = np.zeros_like(num_regions)
for i in range(num_regions):
    print(i)
    if i < num_regions/2:
        region_names[i] = top + str(i) + "_cuboid"
    else:
        region_names[i] = bottom + str(i) + "_cuboid"
        
print(region_names)





##
##print("Enter mean: ")
##mean = input()
##
##print("Enter std: ")
##std = input()
##
##print("Enter num of exchanges: ")
##length = input()
##
#### generate normal distribution
##exchanges = np.random.normal(loc=mean,scale=std,size=length)
##print(exchanges)
##
#### create/edit txt file with 
##file = 
##for i in exchanges:
##    print("Enter index a: ")
##    a = input()
##    print("Enter index b: ")
##    b = input()
##    my_string = "ext_scaleExchange(" + str(a) + "," + str(b) + "," + str(exchanges[i]) + ")\n" 
##    file.write(my_string)
##file.close() 

