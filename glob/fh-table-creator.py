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
    dir_names = sys.argv[1:]
    print(dir_names)
except:
    print("ERROR: Please pass dir_names")
    exit()

for dir, __ in enumerate(dir_names):
    ## pull paths to all .txt files
    os.chdir(dir_names[dir])
    print("Currently in "+dir_names[dir])
    file_names = sorted(glob("*.out/spectrum-new.txt"))

    #print(file_names)

    ## initialize output array
    num_fields = len(dir_names[dir])
    #num_hzs = len()
    current_fh_table = np.zeros([num_fields,1250])

    for field, __ in enumerate(file_names):
        current_table = np.loadtxt(file_names[field],skiprows=1,unpack=True) ## unpack=True --> returns transpose for easier indexing
        current_fh_table[field] = current_table[5] ## 5th index is the full mag() values

    ## transpose array for MPL
    # current_fh_table = current_fh_table.T
    np.savetxt("fh_table.txt",current_fh_table.T,delimiter="\t")
    print("Data table saved at ./"+dir_names[dir]+"fh_table.txt")
    
    os.chdir("..")

print("Finished! Have fun plotting data :-)")
