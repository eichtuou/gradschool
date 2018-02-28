#!/bin/bash
#
# Author: Jessica M. Gonzalez-Delgado
#		  North Carolina State University
#
# This script sets up cube files to be read by a pymol script that 
# generates png files of the orbitals of a molecule, then organizes 
# the png files in directories by isovalues of the surfaces.
#
# Run as: ./mkorbs.sh
#

# molecule name
cname="febpycn4s_monoCA_mo"

# range of orbitals
for i in {69..71}
do
    # pymol only reads cube files
    # cub and cube are the same
    cub=$cname"$i".cub
    cube=$cname"$i".cube
    mv $cub $cube
done

# call pymol script
python2.7 pymol_orbs.py

# organize png files by iso values
declare -a iso=("0.01" "0.02" "0.03" "0.04" "0.05" "0.06" "0.008")
for i in "${iso[@]}"
do
    newdir=iso_"$i"
    mkdir $newdir
    mv ./*"$i".png ./$newdir/
done

