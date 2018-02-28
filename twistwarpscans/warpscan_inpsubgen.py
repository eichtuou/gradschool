'''
Author: Jessica M. Gonzalez-Delgado
		North Carolina State University

This script edits input files for a potential energy surface scan and
generates subission scripts for the calculations.

Run as: python warpscan_inpsubgen.py
'''

#------- User input section -----------!
subs='i'                #substituent
queue='cos'             #name of queue
time='96:00'            #computing time
#--------------------------------------!

import os
import shutil as sh 


# name of complex  
comp='fetpy2_'+subs


# adjust basis set for each case
if subs == 'par':
    basis1=''
    basis2=''
if subs == 'f':
    basis1='F '
    basis2=''
if subs == 'cl':
    basis1='Cl '
    basis2=''
if subs == 'br':
    basis1='Br '
    basis2=''
if subs == 'i':
    basis1=''
    basis2='I 0\nSDD\n****\n'
basis0='\
\n\n\
C H N '+basis1+'0\n\
6-311g*\n\
****\n\
Fe 0\n\
SDD\n\
****\n'+basis2+'\
\n\
FE 0\n\
SDD\n'+basis2[:-6]+'\
\n\
\n'

# get info, generate new input files and submission scripts 
for i in range(0,23):
    for j in range(0,10):
        if i == 22 and j > 0:
            break 
        ifile=comp+'_'+str(i)+'p'+str(j)+'.com'
        sfile='subg09_'+str(i)+'p'+str(j)
        header='\
%chk='+ifile[:-4]+'.chk\n\
%mem=24GB\n\
%nprocshared=12\n\
# p b3lyp/gen\n\
    empiricaldispersion=gd2\n\
    pseudo=cards\n\
    integral=ultrafine\n\
    scrf(pcm,solvent=water,read)\n\
    scf(maxconventionalcycles=100,xqc)\n\
    nosymm\n\
    opt=cartesian\n\
\n\
'+comp+'\n\n'

        # get coordiantes
        with open(ifile,'r') as fo:
            buff=fo.read().split('\n\n')
            buff=buff[2]
        # create backup
        sh.move(ifile, ifile+'~')

        # write new input file
        with open(ifile,'w') as fo: 
            fo.write(header)
            fo.write(buff)
            fo.write(basis0)
            if subs == 'i':
                fo.write('\n')

        # generate submission scripts
        with open(sfile,'w') as fo:
            buff='\
#!/usr/bin/bash\n\
#BSUB -R span[ptile=12]\n\
#BSUB -R "model != L5535"\n\
#BSUB -R "mem>24100"\n\
#BSUB -q '+queue+'\n\
#BSUB -W '+time+'\n\
#BSUB -n 12\n\
#BSUB -J '+str(i)+'p'+str(j)+'_'+subs+'\n\
#BSUB -o output\n\
#BSUB -e error\n\
\n\
echo jobid = $LSB_JOBID\n\
echo hosts = $LSB_HOSTS\n\
\n\
date\n\
g09 '+ifile+'\n\
date\n\n'

            fo.write(buff)
            fo.close()
        # make file executable
        os.chmod('./'+sfile,0755)

