'''
This script generate submission scripts for points in a potential energy surface
'''
import sys
import os

comp='par'
lst=[150,155,160,165,170,175]

for i in range(140,180):
    if i in lst:
        continue 
    filename='subg09_'+str(i)
    fo=open(filename, 'w')
    buff='\
#!/usr/bin/bash\n\
#BSUB -R span[ptile=12]\n\
#BSUB -R "model != L5535"\n\
#BSUB -R "mem>24100"\n\
#BSUB -q single_chassis\n\
#BSUB -W 96:00\n\
#BSUB -n 12\n\
#BSUB -J '+str(i)+'_'+comp+'\n\
#BSUB -o output\n\
#BSUB -e error\n\
\n\
echo jobid = $LSB_JOBID\n\
echo hosts = $LSB_HOSTS\n\
\n\
date\n\
g09 fetpy2q_'+comp+'_'+str(i)+'.com\n\
date\n\n'
    fo.write(buff)
    fo.close()
    os.chmod('./'+filename,0755)

