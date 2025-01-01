# This script organizes Raman spectra files for further analysis.
#   - It renames the spectra of the samples and toluene references,
#     and groups them in their respective data directories.
#   - Specta files must be named as "sampleprefix-sampleinfo-tolspec_1.txt".
#        Example: s0p0-a1-t1_1.txt
#           - sampleprefix = s0p0
#           - sampleinfo = a1 = sample "a", "1st raman spec"
#           - tolpec = t1 = "1st toluene spec" = t1.tol
#           - *_1.txt = default suffix appened by the spectra software
#        Example: dhpb-d4-t3_1.txt
#           - sampleprefix = dhpb
#           - sampleinfo = d4 = sample "d", "4th raman spec"
#           - tolpec = t3 = "3rd toluene spec" = t3.tol

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

