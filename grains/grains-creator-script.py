## Autogenerate graining in mumax
## Stephen Iota
import os
import numpy as np

## Materials
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



## Initialize Different Regions in mumax
## Initialize Different Regions in mumax
my_regions = []

for i in range(num_regions):
    if i < num_regions/2:
        my_regions.append(mumax_region(i, top + str(i) + "_cuboid", top_msat, top_aex))
    else:
        my_regions.append(mumax_region(i, bottom + str(i) + "_cuboid", bottom_msat,bottom_aex))








## Variables for shape definition
dims = (num_regions-2)/2
# create/edit script
script = open("mumax-script.txt","w")
script.write("// Variables for shape definition \n")
for i in range(num_regions):
    if i == 0:
        my_string = region_names[i] + " := cuboid(length,width,t_" + top + ").transl(0,0,(thickness/2-(1/2)*t_"+ top + "))\n"
        script.write(my_string)
    ## top; odd index --> -y-axis
    elif i < num_regions/2 and i % 2 != 0:
        my_string = region_names[i] + " := cuboid(length/" + str(dims) +  " , " + "width/" + str(dims) + ", Zz).transl(length/2 - length/" + str(2*dims) +  ",-width/4,zz)\n"
        script.write(my_string)
    ## top; even index --> +y-axis
    elif i < num_regions/2:
        my_string = region_names[i] + " := cuboid(length/"+ str(dims) +  " , " + "width/" + str(dims) + ", Zz).transl(length/2 - length/" + str(dims*2) + ",width/4,zz)\n"
        script.write(my_string)
    # bot; odd index --> -y-axis
    elif i < num_regions -1 and i % 2 != 0:
        my_string = region_names[i] + " := cuboid(length/"+ str(dims) +  " , " + "width/" + str(dims) + ", Zz).transl(length/2 - length/" + str(dims*2) + ",-width/4,0)\n"
        script.write(my_string)
    ## bot; even index --> +y-axis
    elif i < num_regions - 1:
        my_string = region_names[i] + " := cuboid(length/"+ str(dims) +  " , " + "width/" + str(dims) + ", Zz).transl(length/2 - length/" + str(dims*2) + ",width/4,0)\n"
        script.write(my_string)
    else:
        my_string = region_names[i] + " := cuboid(length,width,t_" + bottom + ").transl(0,0,-(thickness/2-(1/2)*t_"+ bottom + "))\n"
        script.write(my_string)


# Define Regions
script.write("\n// Define Regions\n")
for i in range(num_regions):
    script.write("DefRegion.(" + str(i) + "," + str(region_names[i]) + ")\n")




# Set MSat & AEx
script.write("\n// Material Parameters\n")
for i in range(num_regions):
        if i < num_regions/2:
            script.write("MSat.SetRegion("+str(i)+"," + str(top_msat) + ")")
            script.write("Aex.SetRegion("+str(i)+"," + str(top_aex) + ")")
        else:
            script.write("MSat.SetRegion(i," + str(bottom_msat) + ")")
            script.write("Aex.SetRegion(i," + str(bottom_aex) + ")")











script.close()
