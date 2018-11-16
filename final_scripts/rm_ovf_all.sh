#!/bin/bash

for folder in `find -name "*.out*" -type d`
do
  echo "The current folder is $pwd/$folder" 
  cd $folder
  rm *.ovf
  cd ..
done
