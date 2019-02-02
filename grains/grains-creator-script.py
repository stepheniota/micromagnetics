## Autogenerate graining in mumax
## Stephen Iota
import os, sys
import numpy as np
import argparse

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
num_regions = int(66)
print("Number of regions: " + str(num_regions))

## Class Definitions for mumax Regions
class mumax_region:

    alpha = "alphaFree"

    def __init__(self, RegionNumber, RegionName='name', MSat=0.0, AEx=0.0, Shape="cuboid"):
        self.name = RegionName
        self.index = RegionNumber
        self.aex = AEx
        self.msat = MSat
        self.shape = Shape

## helper functions
def get_line_number(phrase, file_name):
    with open(file_name) as f:
        for i, line in enumerate(f, 1):
            if phrase in line:
                return i

## Initialize Different Regions in mumax
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


## Position of regions
xsize = (int(num_regions)-2)/4

my_regions[0].pos = "{} := cuboid(length,width,t_{}).transl(0,0,thickness/2 - t_{}/4)".format(my_regions[0].name,top,top)
my_regions[num_regions-1].pos = "{} := cuboid(length,width,t_{}).transl(0,0,-(thickness/2 + t_{}/3)".format(my_regions[num_regions-1].name,bottom,bottom)

## top grains, +x
j = 1
for i in range(1,int(num_regions/4)):
    my_regions[i].pos = "{} := cuboid(length/{},width/2,Zz).transl(length/2 - {}*length/(2*{}),width/4,thickness/2 - 3*t_{}/4)".format(my_regions[i].name,xsize,j,xsize,top)
    j = j + 2

## top grains, -x
j = 1
for i in range(int(num_regions/4),int(num_regions/2)):
    my_regions[i].pos = "{} := cuboid(length/{},width/2,Zz).transl(length/2 - {}*length/(2*{}),-width/4,thickness/2 - 3*t_{}/4)".format(my_regions[i].name,xsize,j,xsize,top)
    j = j + 2

## bottom grains, +x
j = 1
for i in range(int(num_regions/2),int(3*num_regions/4)):
    my_regions[i].pos = "{} := cuboid(length/{},width/2,Zz).transl(length/2 - {}*length/(2*{}),width/4,0)".format(my_regions[i].name,xsize,j,xsize)
    j = j + 2

## bottom grains, -x
j = 1
for i in range(int(3*num_regions/4),int(num_regions)-1):
        my_regions[i].pos = "{} := cuboid(length/{},width/2,Zz).transl(length/2 - {}*length/(2*{}),-width/4,0)".format(my_regions[i].name,xsize,j,xsize)
    j = j + 2

## Interlayer Exchange
print("For interlayer Exchange\n")
print("Enter mean: ")
mean = float(input())
print("Enter std: ")
std = float(input())
length = num_regions/2

## generate normal distribution
exchanges = np.random.normal(loc=mean,scale=std,size=length)
#print(exchanges)



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


## Alpha
#script.write("\n//Set Alpha \n")
#for i in range(num_regions):
#    my_alph = "alpha.SetRegion({},{})\n".format(my_regions[i].name,my_regions[i].alpha)
#    script.write(my_alph)

## Interlayer Exchange
script.write("\n// Manipulate Interlayer Exchange\n")
for i in range(1,int(num_regions/2)):
    #int_ext1 = "ext_ScaleExchange({},{},{})\n".format(my_regions[i].index,my_regions[i+1].index,exchanges[i])
    int_ext2 = "ext_ScaleExchange({},{},{})\n".format(my_regions[i].index,my_regions[i+int(num_regions/2 -1)].index,exchanges[i])
    script.write(int_ext2)
script.close()



##mumax_script = sys.argv[1]
##line_num = get_line_number("// PYTHON", mumax_script)
##
##f = open(mumax_script,'r')
##old_script = f.readlines()
##f.close()
##
##grains = open("mumax_script.txt",'r')
##
##old_script.insert(line_num, grains)
##
##f = open(mumax_script, "w")
##new_script = "".join(grains)
##f.write(new_script)
##f.close
##grains.close
##
##os.remove("mumax_script.txt")





## End script
