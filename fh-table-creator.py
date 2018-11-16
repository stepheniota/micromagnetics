#!/usr/bin/python3.5

## Code generates a single `fh_table.txt` file ready for MagicPlot
## after having run `pwsp_all.sh` to process .ovf files
## Stephen Iota
## last updated: 11-2018
##################################################################

import sys, os
import numpy as np
from glob import glob

## pass in dir with .out folders when running script
try:
    dir_name = sys.argv[1:]
    print(dir_name)
except:
    print("ERROR: Please pass dir_name")
    exit()

for dir, __ in enumerate(dir_name):
    ## pull paths to all .txt files
    os.chdir(dir_name[dir])
    print(dir_name[dir])
    file_names = sorted(glob("*.out/spectrum-new.txt"))

    #print(file_names)

    ## initialize output array
    fh_table = np.zeros([10,1250])

    for field, __ in enumerate(file_names):
        ## unpack=True --> returns transpose for easier indexing
        current_table = np.loadtxt(file_names[field],skiprows=1,unpack=True)
        fh_table[field] = current_table[5] ## 5th index is the full mag() values

    ## transpose array for MPL
    fh_table = fh_table.T
    np.savetxt("fh_table.txt",fh_table,delimiter="\t")

    print("Data table saved at ./"+dir_name[dir]+"fh_table.txt")
    os.chdir("..")

print("Finished!")

