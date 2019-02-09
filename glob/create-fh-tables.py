#!/usr/bin/python3.5

## Code generates a single `fh_table.txt` file ready for MagicPlot
## after having run `pwsp_all.sh` to process .ovf files
## Stephen Iota
## last updated: 02-2019

import sys, os, re
import numpy as np
from glob import glob


def alph_to_int(text):
    return int(text) if text.isdigit() else text

def my_sort_key(text):
    return [ alph_to_int(c) for c in re.split(r'(\d+)', text) ]


file_names = glob("*.out/spectrum-new.txt")
file_names.sort(key=my_sort_key)
print(file_names)

## initialize output array
num_fields = len(file_names)
num_hzs = len(np.loadtxt(file_names[0],skiprows=1,unpack=True)[0,:])
current_fh_table = np.zeros([num_fields+1,num_hzs]) ## change depending on time

for field, __ in enumerate(file_names):
    if field == 0:
        current_table = np.loadtxt(file_names[field],skiprows=1,unpack=True)
        current_fh_table[0] = current_table[1] # Hz values
        current_fh_table[1] = current_table[5]
    else:
        current_table = np.loadtxt(file_names[field],skiprows=1,unpack=True)
        ## unpack=True --> returns transpose for easier indexing
        current_fh_table[field+1] = current_table[5] ## 5th index is the full mag() values

## transpose array for MPL
current_fh_table = current_fh_table.T
np.savetxt("fh_table.txt",current_fh_table,delimiter="\t")
print("Data table saved at ./fh_table.txt")

print("Finished! Have fun plotting data ")
