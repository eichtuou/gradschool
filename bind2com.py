'''
This script converts a bind file into a com file.
'''
import sys
from itertools import islice

# check 
if len(sys.argv) == 1:
    print "Error! No bind file specified."
    print "Exiting now..."
    sys.exit()
bindfile=str(sys.argv[1])
if bindfile[-5:] != ".bind": 
    print "Error! File is not bind format."
    print "Exiting now..."
    sys.exit()
else:
    comfile=bindfile[:-5]+'.com'


# get lines of interest from bind file
def get_index(ifile):
    flags=[]
    with open(bindfile,'r') as fo:
        jump=False 
        for num,line in enumerate(fo,1):
            if "Geometry Crystallographic" in line:
                flags.append(num) 
            elif "&" in line:
                if jump == False:
                    flags.append(num) 
                    jump=True 
            elif "Crystal Spec" in line:
                flags.append(num)
    return flags


# get lattice coordiantes 
def get_lattice(ifile,flags):
    a=0.0
    b=0.0
    c=0.0
    with open(ifile) as lines:
        for line in islice(lines,flags[-1],flags[-1]+1):
            buff=line.strip().split()
            a+=float(buff[0])
            b+=float(buff[1])
            c+=float(buff[2])
    a=format(a,'.9f')
    b=format(b,'.9f')
    c=format(c,'.9f')
    return a,b,c


# get atoms and coordinates
def get_atoms(ifile,flags,abc):
    atoms=[]
    with open(ifile) as lines:
        # this will get line index[i]+1 until line index[j]
        # total num lines = index[j] - index[i]+1)
        for line in islice(lines,flags[0]+1,flags[1]-1):
            buff=line
            buff=buff.strip().split()
            del buff[0]
            buff[1]=float(buff[1])*float(abc[0])
            buff[2]=float(buff[2])*float(abc[1])
            buff[3]=float(buff[3])*float(abc[2])
            buff[1]=format(buff[1],'.9f')
            buff[2]=format(buff[2],'.9f')
            buff[3]=format(buff[3],'.9f')
            buff=' '.join(map(str,buff))
            atoms.append(buff)
    return atoms


# make com file
def make_comfile(ifile,atoms,lattice):
    header="# hf/sto-3g\n\n"+ifile[:-4]+"\n\n0 1\n"
    zeros='0.000000000'
    comfile=open(ifile,'w')
    comfile.write(header)
    for i in range(0,len(atoms)):
        comfile.write(atoms[i])
        comfile.write('\n')
    for i in range(0,len(lattice)):
        if i == 0:
            buff='Tv '+str(lattice[i])+' '+zeros+' '+zeros
        elif i == 1:
            buff='Tv '+zeros+' '+str(lattice[i])+' '+zeros
        elif i == 2:
            buff='Tv '+zeros+' '+zeros+' '+str(lattice[i])
        comfile.write(buff)
        comfile.write('\n')
    comfile.close()



# run program
lattice=get_lattice(bindfile,get_index(bindfile))
atoms=get_atoms(bindfile,get_index(bindfile),lattice)
make_comfile(comfile,atoms,lattice)
    
