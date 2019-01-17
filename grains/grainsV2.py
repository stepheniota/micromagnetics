#!/usr/bin/python3.5

## Autogenerate graining in mumax
## Stephen Iota

import os
import numpy as np

## Materials
print("Enter top material: ")
top = input()
print(top)
print("Enter top material MSat: ")
top_msat = float(input())
print("Enter top material AEx: ")
top_aex = float(input())

print("Enter bottom material: ")
bottom = str(input())
print("Enter bottom material MSat: ")
bottom_msat = float(input())
print("Enter bottom material Aex: ")
bottom_aex = float(input())

## Number of grids
#print("Enter number of material regions (num-2 must be a factor of 1024): ")
#num_regions = int(input())
num_regions = 130
print("Number of regions: " + str(num_regions))

#########################################
## Class Definitions for mumax Regions ##
#########################################
class mumax_region:
    
    alpha = "alphaFree"
    
    def __init__(self, RegionNumber, RegionName='name', MSat=0.0, AEx=0.0, Shape="cuboid"):
        self.name = RegionName
        self.index = RegionNumber
        self.aex = AEx
        self.msat = MSat
        self.shape = Shape


###########################################
## Initialize Different Regions in mumax ##
###########################################
my_regions = []

for i in range(num_regions):
    if i < num_regions/2:
        my_regions.append(mumax_region(i))
        my_regions[i].name = top + "{}_cuboid".format(i)
        my_regions[i].aex = top_aex
        my_regions[i].msat = top_msat
    else:
        my_regions.append(mumax_region(i))
        my_regions[i].name = bottom + "{}_cuboid".format(i)
        my_regions[i].aex = bottom_aex
        my_regions[i].msat = bottom_msat




##########################
## Positions of regions ##
##########################
size = (num_regions-2)/2

## top most layer
my_regions[0].pos = "{} := cuboid(length,width,t_{}).transl(0,0,thickness/2 - t_{}/4)\n".format(my_regions[0].geom,top,top)

## bottom most layer
my_regions[num_regions-1].pos = "{} := cuboid(length,width,t_{}).transl(0,0,thickness/2 - t_{}/2)\n".format(my_regions[num_regions-1].geom,bottom,bottom)

j = 0
for i in range(1,num_regions/4):
    my_regions[i].pos = "{} := cuboid(length/{},width/{},Zz).transl(0,0,thickness/2 - t_{})\n".format(my_regions[i].geom,size,size,top)


for i in range(num_regions):
    if i == 0:
        my_regions[i].pos = "{} := cuboid(length,width,t_{}).transl(0,0,thickness/2 - t_{}/2)\n".format(my_regions[i].geom,top,top)
        #my_regions[i].pos = my_regions[i].geom + " := cuboid(length,width,t_" + top + ").transl(0,0,(thickness/2-(1/2)*t_"+ top + "))\n"
    
    elif i == num_regions - 1:
        my_regions[i].pos = my_regions[i].geom + " := cuboid(length,width,t_" + bottom + ").transl(0,0,-(thickness/2-(1/2)*t_"+ bottom + "))\n"
    
    ## top; odd index --> -y-axis
    elif i < num_regions/2 and i % 2 != 0:
        my_regions[i].pos = my_regions[i].geom + " := cuboid(length/" + str(size) +  " , " + "width/" + str(size) + ", Zz).transl(length/2 - length/" + str(2*size) +  ",-width/4,zz)\n"
        
    ## top; even index --> +y-axis
    elif i < num_regions/2:
        my_regions[i].pos = my_regions[i].geom + " := cuboid(length/"+ str(size) +  " , " + "width/" + str(size) + ", Zz).transl(length/2 - length/" + str(size*2) + ",width/4,zz)\n"
    
    ## bot; odd index --> -y-axis
    elif i < num_regions -1 and i % 2 != 0:
        my_regions[i].pos = my_regions[i].geom + " := cuboid(length/"+ str(size) +  " , " + "width/" + str(size) + ", Zz).transl(length/2 - length/" + str(size*2) + ",-width/4,0)\n"
        
    ## bot; even index --> +y-axis
    elif i < num_regions - 1:
        my_regions[i].pos = my_regions[i].geom + " := cuboid(length/"+ str(size) +  " , " + "width/" + str(size) + ", Zz).transl(length/2 - length/" + str(size*2) + ",width/4,0)\n"


#########################
## Interlayer Exchange ##
#########################
print("For interlayer Exchange\n")
print("Enter mean: ")
mean = float(input())
print("Enter std: ")
std = float(input())
length = 100000

## generate normal distribution
exchanges = np.random.normal(loc=mean,scale=std,size=length)
#print(exchanges)





########################
### Print Statements ###
########################
script = open("mumax-script.txt","w")

## Variables for Shape Definition
script.write("// Variables for Shape Definition\n")
for i in range(num_regions):
    shape = "{} := {}\n".format(my_regions[i].name,my_regions[i].shape)
    script.write(shape)
script.write("\n")

## Set Geometry
script.write("//Set Geometry\n")
geom = "SetGeom("
for i in range(num_regions-1):
    geom += my_regions[i].name + ".add("
geom += my_regions[num_regions-1].name
geom += (num_regions+1)*")" + ("\n \n")
script.write(geom)
script.write("\n \n")

## Define Regions
script.write("//Define Regions\n")
for i in range(num_regions):
    region = "DefRegion({},{})\n".format(my_regions[i].name,my_regions[i].index)
    script.write(region)
script.write("\n \n")

## Material Parameters
script.write("\n //Material Parameters \n")
for i in range(num_regions):
    mat_param = "Msat.SetRegion({},{}) //{}\n".format(my_regions[i].index,my_regions[i].msat,my_regions[i].name)
    script.write(mat_param)
    aex_param = "Aex.SetRegion({},{}) //{}\n".format(my_regions[i].index,my_regions[i].aex,my_regions[i].name)
    script.write(aex_param)
    
    
## Alpha
script.write("\n\\Set Alpha \n")
for i in range(num_regions):
    my_alph = "alpha.SetRegion({},{})\n".format(my_regions[i].name,my_regions[i].alpha)
    script.write(my_alph)
    
## Interlayer Exchange
script.write("\n\\\\Manipulate Interlayer Exchange\n")    
for i in range(1,int(num_regions/2)):
    int_ext1 = "ext_ScaleExchange({},{},{})\n".format(my_regions[i].index,my_regions[i+1].index,exchanges[i])
    int_ext2 = "ext_ScaleExchange({},{},{})\n".format(my_regions[i].index,my_regions[i+int(num_regions/2)].index,exchanges[i])
    script.write(int_ext1 + int_ext2)


    
script.close()

#End script












