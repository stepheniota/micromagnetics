#!/usr/bin/python3.5
## Autogenerate graining in mumax
## Stephen Iota

## Notes
# Make sure MuMax script has unit cell dimension variables (Xx, Yy, Zz) defined, if not refer to scripts in /data/Stephen/PyYig/Grains
# as well as follows our standard convention for script variables

import os, sys
import numpy as np
import argparse

## USER OPTIONS
num_regions = int(10) # value must be two more than a multiple of four (num_regions = 2 + 4n)
top = "py"
top_msat = 800e3
top_aex = 1.3e-11
bottom = "yig"
bottom_msat = 175e3
bottom_aex = 3.5e-12
mean_coupling = 0.8
std_coupling = 0.02 ## standard deviation of coupling centered around mean_coupling
varyCoupling = False #easy way to set std_coupling = 0
## END USER OPTIONS

## Useful variables
num_grains = int(num_regions - 2) #subtracting top and bottom regions
ysize = int(num_grains)/4 #size of grains along axis of wire is fixed to 1/2 of wire width

## Class Definitions for mumax Regions
class mumax_region:
    #alpha = "alphaFree"
    def __init__(self, RegionNumber, RegionName='name', MSat=0.0, AEx=0.0, Shape="cuboid"):
        self.name = RegionName
        self.index = RegionNumber
        self.aex = AEx
        self.msat = MSat
        self.shape = Shape
        #self.alpha = ###alphaFree
## Initialize Different Regions in mumax
my_regions = []
for i in range(num_regions):
    if i < num_regions/2:
        my_regions.append(mumax_region(i))
        my_regions[i].name = "{}_cuboid{}".format(top,i)
        my_regions[i].aex = top_aex
        my_regions[i].msat = top_msat
    else:
        my_regions.append(mumax_region(i))
        my_regions[i].name = "{}_cuboid{}".format(bottom,i)
        my_regions[i].aex = bottom_aex
        my_regions[i].msat = bottom_msat


## Top and bottom main regions
### modify this line depending on thickness of yig and py layers
my_regions[0].pos = "{} := cuboid(length,width,t_{}/2).transl(0,0,thickness/2 - t_{}/4)".format(my_regions[0].name,top,top)
my_regions[num_regions-1].pos = "{} := cuboid(length,width,2*t_{}/3).transl(0,0,-thickness/2 + t_{}/3)".format(my_regions[num_regions-1].name,bottom,bottom)
## top grains, +x
j = 1
for i in range(1,int(num_grains/4) + 1):
    my_regions[i].pos = "{} := cuboid(length/{},width/2,Zz).transl(length/2 - {}*length/{},width/4,thickness/2 - 3*t_{}/4)".format(my_regions[i].name,ysize,j,2*ysize,top)
    j = j + 2
## top grains, -x
j = 1
for i in range(int(num_grains/4) + 1 ,int(num_grains/2) + 1):
    my_regions[i].pos = "{} := cuboid(length/{},width/2,Zz).transl(length/2 - {}*length/{},-width/4,thickness/2 - 3*t_{}/4)".format(my_regions[i].name,ysize,j,2*ysize,top)
    j = j + 2
## bottom grains, +x
j = 1
for i in range(int(num_grains/2) + 1, 3*int(num_grains/4) + 1):
    my_regions[i].pos = "{} := cuboid(length/{},width/2,Zz).transl(length/2 - {}*length/{},width/4,-thickness/2+5*t_{}/6)".format(my_regions[i].name,ysize,j,2*ysize,bottom)
    j = j + 2
## bottom grains, -x
j = 1
for i in range(3*int(num_grains/4) + 1,int(num_grains) + 1):
    my_regions[i].pos = "{} := cuboid(length/{},width/2,Zz).transl(length/2 - {}*length/{},-width/4,-thickness/2+5*t_yig/6)".format(my_regions[i].name,ysize,j,2*ysize,bottom)
    j = j + 2


## Interregion exchanges
exchanges = []
for grain in range(int(num_regions/2),int(num_regions)):
    current = "ext_ScaleExchange(0,{},{})".format(grain,mean_coupling)
    exchanges.append(current)
for grain in range(1,int(num_regions/2)):
    current = "ext_ScaleExchange({},{},{})".format(num_regions-1,grain,mean_coupling)
    exchanges.append(current)
for region in range(1,int(num_regions/2)):
    for j in range(int(num_regions/2),int(num_regions)):
        if varyCoupling:
            new_coupling = np.random.normal(loc=mean_coupling,scale=std_coupling)
            current = "ext_ScaleExchange({},{},{})".format(region,j,new_coupling)
        else:
            current = "ext_ScaleExchange({},{},{})".format(region,j,mean_coupling)
        exchanges.append(current)

## Print Statements
script = open("mumax_script.txt","w")
## Variables for Shape Definition
script.write("// Variables for Shape Definition\n")
for i in range(num_regions):
    shape = "{}\n".format(my_regions[i].pos)
    script.write(shape)
script.write("\n")

## Set Geometry
script.write("//Set Geometry\n")
geom = "SetGeom("
for i in range(num_regions-1):
    geom += my_regions[i].name + ".add("
geom += my_regions[num_regions-1].name
geom += (num_regions)*")" + ("\n \n")
script.write(geom)
script.write("\n")
script.write("saveas(geom, \"geom\")\n")


## Define Regions
script.write("//Define Regions\n")
for i in range(num_regions):
    region = "DefRegion({},{})\n".format(my_regions[i].index,my_regions[i].name)
    script.write(region)
script.write("\n")
script.write("snapshot(Regions)\n")

script.write("/** END GEOMETRY **/ \n")
script.write("/** MATERIAL PARAMETERS **/")

## Material Parameters
script.write("\n //Material Parameters \n")
for i in range(num_regions):
    mat_param = "Msat.SetRegion({},{}) //{}\n".format(my_regions[i].index,my_regions[i].msat,my_regions[i].name)
    script.write(mat_param)
    aex_param = "Aex.SetRegion({},{}) //{}\n".format(my_regions[i].index,my_regions[i].aex,my_regions[i].name)
    script.write(aex_param)

## Interlayer Exchange
script.write("\n// Manipulate Interlayer Exchange\n")
for i, __ in enumerate(exchanges):
    int_ext = exchanges[i]
    script.write(int_ext)
    script.write("\n")

script.close()

## END SCRIPT
