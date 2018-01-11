'''
This script generates example input files and submission scripts for a series of calculations 
from a functional benchmarking. It creates directories for each functional and moves the files 
with the correct permissions to their respective directories.  
'''

import sys
import os
import shutil as sh


funcs=["cc-pVDZ","cc-pVTZ","cc-pVQZ","cc-pV5Z","cc-pV6Z","aug-cc-pVDZ","aug-cc-pVTZ",\
       "aug-cc-pVQZ","aug-cc-pV5Z","aug-cc-pV6Z"]


# generate com files for diferent functionals
def gen_comfiles(funcs):
    comfiles=[]
    for i in funcs: 
        os.mkdir(i)
        comname='h_'+i+'.com'
        comfiles.append(comname)
        src=os.getcwd()+'/'+comname
        dst=os.getcwd()+'/'+comname[2:-4]+'/'+comname
        buff="\
%chk=h_"+i+".chk\n\
%mem=4GB\n\
%nprocs=2\n\
# p hf/"+i+"\n\
\n\
h_"+i+"\n\
\n\
0 1\n\
H      0.000000    0.000000    0.000000\n\
\n"
        with open(comname,'w') as fo:
            fo.write(buff)
        sh.move(src,dst) 


# generate submision scripts 
def gen_subs(funcs):
    for i in funcs:
        subsname='subg09_'+i
        src=os.getcwd()+'/'+subsname
        dst=os.getcwd()+'/'+i+'/'+subsname
        buff='\
#!/usr/bin/bash\n\
#BSUB -R span[ptile=8]\n\
#BSUB -R "model != L5535"\n\
#BSUB -R "mem>16100"\n\
#BSUB -q debug\n\
#BSUB -n 2\n\
#BSUB -W 00:05\n\
#BSUB -J '+i+'\n\
#BSUB -o output\n\
#BSUB -e error\n\
\n\
echo jobid = $LSB_JOBID\n\
echo hosts = $LSB_HOSTS\n\
\n\
date\n\
g09 h_'+i+'.com\n\
date\n\
\n'
        with open(subsname,'w') as fo:
            fo.write(buff)
            os.chmod('./'+subsname,0755)
        sh.move(src,dst) 



# RUN PROGRAM
gen_comfiles(funcs)
gen_subs(funcs)

