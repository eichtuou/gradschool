#!/bin/bash
# This script renames multiple input files. Then calls a python script that grabs the
# coordinates from these files, edits them, and generates submission scripts for each.
# Finally the script submits the calculations.

# name of complex 
comp='i'

# rename files so they can be read by the python script
for i in {0..22}
do 
    for j in {0..9}
    do
        if [[ "$i" -eq "22" && "$j" -gt "0" ]]; then
            continue
        fi
        mv "$i"p"$j".com fetpy2_"$comp"_"$i"p"$j".com
    done
done

python warpscan_inpsubgen.py

# submit calculations
for i in {0..22}
do 
    for j in {0..9}
    do
        if [[ "$i" -eq "22" && "$j" -gt "0" ]]; then
            continue
        fi
        echo "$i"p"$j" 
        bsub < subg09_"$i"p"$j"
    done
done

