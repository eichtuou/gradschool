'''
This script generates scripts for making cube files later used 
for creating a gif of the simulation.
'''

import sys
import os


name='febpycn4s_par_cn_a'
wavef=name+'_aligned.bind.edyn.wave'
orbital='L2'
cube=name+'_'+orbital+'_cube'
time_fs=4000
suball=[]


# generate cube and submission scripts
for i in range(0,time_fs+10,10):
    if i == 1:
        continue
    if i == 0:
        j=i+1
    else:
        j=i

    # make cube script
    filename=cube+'_'+str(j)+'.in' 
    buff1='region\n\
0.25\n\
0.0000  15.24749188\n\
0.0000  10.48704607\n\
0.0000  26.00000000\n\
\n\
name\n'+filename[:-3]+'\n\
\n\
make\n1\n'
    fo=open(filename,'w')
    fo.write(buff1)
    fo.write(str(j))
    fo.close()
    os.chmod('./'+filename,0755)
    
    # make submission script 
    sfilename='subcube_'+filename[:-3]
    buff2='\
#!/usr/bin/bash\n\
#BSUB -R span[ptile=8]\n\
#BSUB -R "model != L5535"\n\
#BSUB -R "mem>24100"\n\
#BSUB -q cos\n\
#BSUB -W 24:00\n\
#BSUB -n 2\n\
#BSUB -J '+filename[:-3]+'\n\
#BSUB -o output\n\
#BSUB -e error\n\
\n\
echo jobid = $LSB_JOBID\n\
echo hosts = $LSB_HOSTS\n\
\n\
date\n\
cubebuilder '+filename+' '+wavef+'\n\
date\n\n'
    fo=open(sfilename,'w')
    fo.write(buff2)
    fo.close()
    os.chmod('./'+sfilename,0755)

    # for submitting all jobs at once
    subcmd='bsub < '+sfilename
    suball.append(subcmd)

# generate input stream for bash script
with open('suball.sh','w') as fo:
    for i in range(0,len(suball)):
        fo.write(suball[i])
        fo.write('\n')
os.chmod('./suball.sh',0755)

