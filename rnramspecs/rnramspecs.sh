#!/bin/bash
# 
# Author: Jessica M. Gonzalez-Delgado
#         North Carolina State University
#
# This script organizes Raman spectra files for further analysis. It 
# renames the spectra of the samples and toluene references, and groups
# them in their respective data directories. The specta files must be 
# named as "sampleprefix-sampleinfo-tolspec_1.txt" like s0p0-a1-t1_1.txt
# or dhpb-d4-t3_1.txt. Where `sampleprefix` is a common prefix used for
# identical samples, `sampleinfo` is what specific sample (a1 = sample "a"
# first run, d4 = sample "d" fourth run), and `tolspec` is the toluene 
# reference spectrum (t1 = t1.tol, t3 = t3.tol)
#
# Run as: bash rnspec.sh


# working directory
wdir=`pwd`

# clean directory
# these are binary files from the raman software
rm -fr *.SPE

# toluene spectra directory
mkdir tol

# rename spectra files
for file in $( ls $wdir )
do
    if [ -f $file ]
    then
        # skip script and experimental setup files
        if [[ $file == "rnramspec.sh" || $file == "exp.dat" || $file == "samples.dat" || $file == "tol.dat" ]]
        then
            continue

        # rename and organize toluene spectra
        # changing them from t*_1.txt to t*.tol
        elif [[ ${file:0:1} == "t" ]]
        then
            temp=`echo $file | cut -d _ -f 1`".tol"
            mv $file tol/$temp

        # rename other spectra
        # changing from *_1.txt to *.txt
        else
            nfile=`echo $file | cut -d _ -f 1`".txt"
            mv $file $nfile

            # organize spectra by samples & toluene standard
            smpl=`echo $nfile | cut -d - -f 1`
            tol=`echo $nfile | cut -d . -f 1 | rev | cut -d - -f 1 | rev`
            if [[ ! -d $wdir/$smpl ]]; then
                mkdir $wdir/$smpl
            fi 
            if [[ ! -d $wdir/$smpl/$tol ]]; then
                mkdir $wdir/$smpl/$tol
            fi 
            mv $wdir/$nfile $wdir/$smpl/$tol/
        fi
    fi
done

