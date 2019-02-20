#!/usr/bin/python3.5

## Code generates a fh_table for colorplot
## after having run mumax pwsp to fft data
## Stephen Iota
## last updated: 02-2019

import sys, os, re
import numpy as np
from glob import glob

## variables
mag = 5 ## 2 = mx, 3 = my, 4 = mz, 5 = mfull
mirror = True ## do you want fh_table with negative field values?

## sorting helper functions
def alph_to_int(text):
    return int(text) if text.isdigit() else text

def my_sort_key(text):
    return [ alph_to_int(c) for c in re.split(r'(\d+)', text) ]

file_names = glob("*.out/spectrum-new.txt")
file_names.sort(key=my_sort_key)
#print(file_names)
## initialize output array
num_fields = len(file_names)
num_hzs = len(np.loadtxt(file_names[0],skiprows=1,unpack=True)[0,:])
#num_hzs = 1250
fh_table = np.zeros([num_fields+1,num_hzs])

first = True
for field, __ in enumerate(file_names):
    current_table = np.loadtxt(file_names[field],skiprows=1,unpack=True) ## unpack=True --> returns transpose for easier indexing
    if first:
        fh_table[0] = current_table[1] # Hz values
        first= False
    fh_table[field+1] = current_table[mag] ## 5th index is the full mag() values



## for fh_plt with negative field values
if mirror:
    mirrored_fh_table = np.zeros([2*num_fields,num_hzs])
    negative_fields = fh_table[2:][::-1]
    mirrored_fh_table[0] = fh_table[0]
    mirrored_fh_table[1:num_fields] = negative_fields
    mirrored_fh_table[num_fields:] = fh_table[1:]
    mirrored_fh_table = mirrored_fh_table.T
    np.savetxt("mirrored_fh_table.txt",mirrored_fh_table,delimiter='\t')

## transpose arrays for MPL
fh_table = fh_table.T
np.savetxt("fh_table.txt",fh_table,delimiter="\t")

print("Finished! Have fun plotting data :-)")
