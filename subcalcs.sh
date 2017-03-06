#!/usr/bin/bash

# This script submits multiple submission scripts into the cluster. It calls a python 
# script that generates the submission scripts for each calculation, then organizes the 
# calculations in individual directories and submits the calculations from each directory. 

# master path
mypath=`pwd`

# generate submission scripts
python scriptsgen.py

declare -a comp=("fetpy2")
declare -a state=("singlet" "triplet" "quintet" "heptet")
declare -a sust=("par" "br" "cl" "f" "i")

for i in "${sust[@]}"
do
    for j in "${state[@]}"
    do   
        for k in "${comp[@]}"
        do
            cd $mypath
            # directories for calculations already exist
            mv subg09_"$k"${j:0:1}_$i $mypath/"$k"_$i/$j/
            cd $mypath/"$k"_$i/$j
            pwd
            bsub < subg09_"$k"${j:0:1}_$i
        done
    done
done

