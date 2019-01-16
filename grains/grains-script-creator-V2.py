## Autogenerate graining in mumax
## V2
## Stephen Iota

import os
import numpy as np


## Class Definitions for mumax Regions
class region:
  def __init__(self, RegionName, MSat, AEx):
      self.name = RegionName
      self.aex = AEx
      self.msat = MSat

## Materials User Input
print("Enter top material: ")
top = input()
print(top)
print("Enter top material MSat: ")
top_msat = input()
print("Enter top material AEx: ")
top_aex = input()

print("Enter bottom material: ")
bottom = input()
print("Enter bottom material MSat: ")
bottom_msat = input()
print("Enter bottom material Aex: ")
bottom_aex = input()

## Number of grids
#print("Enter number of material regions (num-2 must be a factor of 1024): ")
#num_regions = int(input())
num_regions = 130
print("Number of regions: " + str(num_regions))


## Set Region Info
my_regions = np.zeros(130)


for i in range(num_regions):
    if i < num_regions/2:
        my_regions[i] = region(str(top) + str(i) + "_cuboid", int(top_msat), int(top_aex))
    #else:
    #    my_regions[i] = region(str(bottom) + str(i) + "_cuboid", bottom_msat, bottom_aex)



## Positions of regions
dims = (num_regions-2)/2
for i in range(num_regions):

    if i == 0:
        my_regions[i].pos = my_regions[i].name + " := cuboid(length,width,t_" + top + ").transl(0,0,(thickness/2-(1/2)*t_"+ top + "))\n"

    elif i == num_regions - 1:
        my_regions[i].pos = my_regions[i].name + " := cuboid(length,width,t_" + bottom + ").transl(0,0,-(thickness/2-(1/2)*t_"+ bottom + "))\n"

    ## top; odd index --> -y-axis
    elif i < num_regions/2 and i % 2 != 0:
        my_regions[i].pos = my_regions[i].name + " := cuboid(length/" + str(dims) +  " , " + "width/" + str(dims) + ", Zz).transl(length/2 - length/" + str(2*dims) +  ",-width/4,zz)\n"

    ## top; even index --> +y-axis
    elif i < num_regions/2:
        my_regions[i].pos = my_regions[i].name + " := cuboid(length/"+ str(dims) +  " , " + "width/" + str(dims) + ", Zz).transl(length/2 - length/" + str(dims*2) + ",width/4,zz)\n"

    # bot; odd index --> -y-axis
    elif i < num_regions -1 and i % 2 != 0:
        my_regions[i].pos = my_regions[i].name + " := cuboid(length/"+ str(dims) +  " , " + "width/" + str(dims) + ", Zz).transl(length/2 - length/" + str(dims*2) + ",-width/4,0)\n"

    ## bot; even index --> +y-axis
    elif i < num_regions - 1:
        my_regions[i].pos = my_regions[i].name + " := cuboid(length/"+ str(dims) +  " , " + "width/" + str(dims) + ", Zz).transl(length/2 - length/" + str(dims*2) + ",width/4,0)\n"
