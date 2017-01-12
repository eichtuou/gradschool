'''
This script generate submission scripts for density calculations\
for either of our clusters.
'''

#-------------------- user input section --------------------!
ncubes=288                  # number of total cubes
dtype='scf'                 # type of density 'scf' or 'ci'
dname='ringA'               # name of fchk file 
jname='bh5rA'               # job name
cluster='henry'             # cluster name 'henry' or 'murgas'
#------------------------------------------------------------!

import sys
import os

# check
if cluster != 'henry' and cluster != 'murgas':
    print "Who are you?"
    print "Exiting program..."
    sys.exit()
if ncubes < 1:
    print "Number of cubes has to be equal or greater than 1."
    print "Exiting program..."
    sys.exit()
if dtype != 'scf' and dtype != 'ci':
    print "Verify type of density."
    print "Exiting program..."
    sys.exit()
if len(dname) < 1:
    print "Verify name of fchk file."
    print "Exiting program..."
    sys.exit()

# generate submision scripts
if cluster == 'henry':
    for i in range(1,ncubes+1):
        filename='subcubegen_'+str(i)
        fo=open(filename, 'w')
        buff='\
#!/usr/bin/bash\n\
#BSUB -R span[ptile=8]\n\
#BSUB -R "model != L5535"\n\
#BSUB -R "mem>16100"\n\
#BSUB -q debug\n\
#BSUB -W 0:15\n\
#BSUB -J '+str(jname)+'_'+str(i)+'\n\
#BSUB -o output\n\
#BSUB -e error\n\
\n\
# tells you what hosts you are running on\n\
echo jobid = $LSB_JOBID\n\
echo hosts = $LSB_HOSTS\n\
#setenv OMP_NUM_THREADS 16\n\
\n\
# setup gaussian environment\n\
export g09root=/gpfs_common/share/jmgonza4\n\
source $g09root/g09/bsd/g09.profile\n\
export GAUSS_SCRDIR=`pwd`\n\
export GAUSS_MEMDEF=269000000 # 2 GB\n\
export PATH=/gpfs_common/share/jmgonza4/g09/bsd:/gpfs_common/share/jmgonza4/g09/local:/gpfs_common/share/jmgonza4/g09/extras:/gpfs_common/share/jmgonza4/g09:$PATH\n\
\n\
date\n\
cubegen 1 fdensity='+str(dtype)+' '+str(dname)+'.fchk cube_'+str(i)+'.cube -1 < inp_cube_'+str(i)+'.dat\n\
date\n\n'
        fo.write(buff)
        fo.close()
        os.chmod('./'+filename,0755)

if cluster == 'murgas':
    for i in range(1,ncubes+1):
        filename='subcubegen_'+str(i)
        fo=open(filename, 'w')
        buff='\
#!/bin/bash\n\
#These commands set up the Grid Environment for your job:\n\
#PBS -jeo\n\
#PBS -o output\n\
#PBS -e error\n\
#PBS -N '+str(jname)+'_'+str(i)+'\n\
#PBS -l pmem=2GB,nodes=1:ppn=1,walltime=300:00:00\n\
#########\n\
\n\
# runs job from the current working directory\n\
RUNDIR=$PBS_O_WORKDIR\n\
export RUNDIR\n\
cd $RUNDIR\n\
\n\
# setup gaussian environment\n\
export g09root=/opt/chemistry\n\
source $g09root/g09/bsd/g09.profile\n\
export GAUSS_MEMDEF=269000000 # 2 GB\n\
export PATH=/opt/chemistry/g09:$PATH\n\
\n\
date\n\
cubegen 1 fdensity='+str(dtype)+' '+str(dname)+'.fchk cube_'+str(i)+'.cube -1 < inp_cube_'+str(i)+'.dat\n\
date\n\n'
        fo.write(buff)
        fo.close()
        os.chmod('./'+filename,0755)

