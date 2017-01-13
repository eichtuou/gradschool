'''
This script gets excitations of interest from a TD-DFT calculation.
'''
import sys
import linecache

# give log file as argument
# check
if len(sys.argv) == 1:
    print "Error! No log file specified."
    print "Exiting now..."
    sys.exit()
logfile=str(sys.argv[1])
if logfile[-4:] != ".log": 
    print "Error! File is not log format."
    print "Exiting now..."
    sys.exit()


# start program
print "Reading file: "+logfile
print "..."

# count number of lines in log file
numlines=sum(1 for line in open(logfile))
# get excitations of interest
states=[]
index=[]
for i in range(1,numlines+1):
    line=linecache.getline(logfile,i).strip()
    if 'Excited State' in line:
        line=line.split()
        nm=float(line[6])
        fosc=float(line[8].replace('f=',''))
        if nm >= 350.0 and fosc >= 0.01:
            states.append(int(line[2].replace(':','')))
            index.append(int(i))

# write info to file
outf=open(logfile[:-4]+'_analyzedExcitations.dat','w')
for i in index:
    line=linecache.getline(logfile,i).strip()
    line=line.split()
    buff=str(line[0])+' '+str(line[1])+' '+str(line[2])+'   '+str(line[6])+' '+str(line[7])+'   '+str(line[8])+'\n'
    outf.write(buff)
    occ=[]     # occupied orbitals
    virt=[]     # virtual orbitals
    coeff=[]    # coeffient
    contr=[]    # contribution
    for j in range(1,100):
        k=i
        k+=j
        buff=linecache.getline(logfile,k).strip()
        # get orbital contributions from each excited state
        if '->' in buff:
            buff=buff.replace('->','-> ')
            buff=buff.split()
            buff2=float(buff[3])
            buff2=2*buff2**2
            buff2=format(float(buff2),'.2f')
            buff2=str(buff2)
            occ.append(int(buff[0]))
            virt.append(int(buff[2]))
            coeff.append(buff[3])
            contr.append(buff2)
        if 'Excited State' in buff:
            break
    # sort contributions in ascending virtual orbitals
    virt,occ,coeff,contr=(list(t) for t in zip(*sorted(zip(virt,occ,coeff,contr))))
    for k in range(0,len(occ)):
        buff=str(occ[k])+' -> '+str(virt[k])+'  '+str(coeff[k])+'  contr='+str(contr[k])+'\n'
        outf.write(buff)
    outf.write('\n')
outf.close()
print "Done."
print "Excitations of interest located in "+logfile[:-4]+"_analyzedExcitations.dat"

