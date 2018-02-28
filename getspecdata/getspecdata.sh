#!/bin/bash
# 
# Author: Jessica M. Gonzalez-Delgado
#		  North Carolina State University
#
# This script collects spectral data from a series of different TD-DFT calculations performed to benchmark
# functionals. The data files generated from this script are then used in a GNU plot script to create the 
# images. The script calls a pearl script that fetches the excitations and stores them in a *_sticks.dat file. 
# The script then calls another pearl script that reads the *_sticks.dat file and creates and stores spectral
# information in a *_spec.dat file.
#
# Run as: ./getspecdata.sh
#
 
# parent directory
parent=/Volumes/CALC/henry/functionalBenchmarking
# directory where we will be saving the generated *.dat files 
spec=`pwd`

# array with name of functionals used in the benchmarking 
declare -a fun=("b3lyp" "bhandhlyp" "bp86" "cam-b3lyp" "hfb" "hfs" "lc-bp86" "lc-wpbe" "m06" "m06hf" "m06l" "pbe1pbe")

# we sampled distances from 3 to 10 angstroms
for i in {3..10} 
do
    # access directory with data from the "i" [angs] system 
    systdir=$parent/"$i"a
    cd $systdir 
    for j in "${fun[@]}"
    do
        # access directory of functional
        cd $systdir/$j
        echo "Getting spectral data from " `pwd` 
            gdv_uvvis_sticks.pl bh"$i"_"$j".log > bh"$i"_"$j"_sticks.dat
            sticks2broad.pl bh"$i"_"$j"_sticks.dat 0.12 > bh"$i"_"$j"_spec.dat
            # we want to store data file by functional, not by distance
            if [ "$i" == "3" ]; then
               mkdir $spec/$j 
            fi
            mv *.dat $spec/$j/
    done
done

