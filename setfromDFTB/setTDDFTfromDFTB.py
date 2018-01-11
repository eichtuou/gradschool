'''
This script generates TD-DFT input files from a DFTB conformation scan output.
It also generates submission scripts for each TD-DFT calculation, and an input 
stream file to submit all the jobs at once. 
'''

#---------------USER INPUT SECTION---------------!
cluster='henry'                   # henry, murgas
queue='single_chassis'            # name of queue
prefix='dmonoCA_slab_tarj_'       # complex name
#------------------------------------------------!

import sys
import os
import shutil as sh


# basis set 
basis='\
C H N O 0\n\
6-311g*\n\
****\n\
Fe 0\n\
SDD\n\
F   1   1.00\n\
      2.462\n\
****\n\
\n\
FE 0\n\
SDD\n\
\n\
\n'


# get files in current directory
allfiles=os.listdir(os.getcwd())
comfiles=[]
suball=[] 


# get names of input files
for file in allfiles:
    if prefix in file:
        comfiles.append(file)


# edit input files
for i in comfiles:
    ifile=i                     # input file name
    sfile='subg09_'+ifile[:-4]  # submission script name

    header='\
%chk='+ifile[:-4]+'.chk\n\
%mem=16GB\n\
%nprocshared=8\n\
# p b3lyp/gen\n\
    empiricaldispersion=gd2\n\
    pseudo=cards\n\
    integral=ultrafine\n\
    td(singlets,nstates=30)\n\
    scrf(pcm,solvent=water,read)\n\
    nosymm\n\
\n\
'+ifile[:-4]+'\n\
\n\
-2 1\n'

    # get coordiantes
    with open(ifile,'r') as fo:
        buff=fo.read().split('\n\n')
        buff=buff[2].split('\n')
        del buff[0]
        coords='\n'.join(buff[0:])+'\n\n'

    # create backup
    sh.move(ifile, ifile+'~')

    # write new input file
    with open(ifile,'w') as fo: 
        fo.write(header)
        fo.write(coords)
        fo.write(basis)

    # generate submission scripts
    if cluster == 'henry':
        subtext='\
#!/usr/bin/bash\n\
#BSUB -R "model != L5535"\n\
#BSUB -R span[ptile=8]\n\
#BSUB -R "mem>16100"\n\
#BSUB -q '+queue+'\n\
#BSUB -n 8\n\
#BSUB -W 2:00\n\
#BSUB -J '+ifile[:-4]+'\n\
#BSUB -o output\n\
#BSUB -e error\n\
\n\
echo jobid = $LSB_JOBID\n\
echo hosts = $LSB_HOSTS\n\
\n\
date\n\
g09 '+ifile+'\n\
date\n\n' 
        subcmd='bsub < '+sfile
        suball.append(subcmd)

    if cluster == 'murgas':                                             
        subtext='\
#!/bin/bash\n\
#These commands set up the Grid Environment for your job:\n\
#PBS -jeo\n\
#PBS -o output\n\
#PBS -e error\n\
#PBS -N '+ifile[:-4]+'\n\
#PBS -l pmem=2GB,nodes=1:ppn=8,walltime=300:00:00\n\
#########\n\
\n\
RUNDIR=$PBS_O_WORKDIR\n\
export RUNDIR\n\
cd $RUNDIR\n\
\n\
date\n\
g09 '+ifile+'\n\
date\n\n'
        subcmd='qsub '+sfile
        suball.append(subcmd)
    
    with open(sfile,'w') as fo:
        fo.write(subtext)
    os.chmod('./'+sfile,0755)


# generate input stream for bash script
with open('suball.sh','w') as fo:
    for i in range(0,len(suball)):
        fo.write(suball[i])
        fo.write('\n')
os.chmod('./suball.sh',0755)

