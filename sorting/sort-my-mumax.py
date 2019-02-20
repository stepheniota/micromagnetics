#!/usr/bin/python3.5
## To sort file names created by `mumax-script-creator-field`
## Stephen Iota
## 02-2019

import os, sys
import re
from glob import glob


def alph_to_int(text):
    return int(text) if text.isdigit() else text

def sorting_key(text):
    return [ alph_to_int(c) for c in re.split(r'(\d+)', text) ]

file_names = glob("*.out/spectrum-new.txt")
file_names.sort(key=sorting_key)
print(file_names[:20])
