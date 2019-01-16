#!/bin/bash

for folder in `find -name "*.out*" -type d`
do
 	cd $folder
	echo "The current folder is $folder" 
 	rm *.ovf
	cd ..
done
