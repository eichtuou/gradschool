#!/bin/bash
#
# Author: Jessica M. Gonzalez-Delgado
#	  North Carolina State University
#
# This script grabs the electronic energy of a series of calculations
# performed for a potential energy surface scan on different halogentated 
# Fe(tpy)2 complexes. It will only output the information if and only if
# the calculation converged.
#
# Run as: bash getSCF.sh > scf.dat


# working directory
wdir=`pwd`

# molecule
mol='fetpy2q_'

# substituents
declare -a subs=("par" "f" "cl" "br" "i")

# points in PES scan 
declare -a pts=("150" "152p5" "155" "157p5" "160" "162p5" "165"\
                 "167p5" "170" "172p5" "175" "177p5" "180" )

# navigate through directories
for i in "${subs[@]}"
do
    if [ $i != "par" ]; then
        printf "\n"
    fi
    echo $i
    # get electronic energy only if calculation converged
    for j in "${pts[@]}"
    do
        cd $wdir/"$mol""$i"/$j
        converged=`grep 'Stationary point found' "$mol""$i"_"$j"".log"`
        if [ ${#converged} -ne "0" ]; then
            printf "$j"
            grep "SCF Done" "$mol""$i"_"$j"".log" | tail -1 
        fi
    done
done    

