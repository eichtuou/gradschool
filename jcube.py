#-------------------- USER INPUT SECTION --------------------!
dname = 'h2o_opt_6-311g+'       # name of fchk file
dtype = 'scf'                   # density type -- ci or scf 
#------------------------------------------------------------!

import sys
import os
import numpy as np
from itertools import product
from itertools import islice 


# used for filling upper triangular part of density matrices
class symNDarray(np.ndarray):
    def __setitem__(self, (i, j), value):
        super(symNDarray, self).__setitem__((i, j), value)                    
        super(symNDarray, self).__setitem__((j, i), value)                    
def symmetrize(arr):
    return arr + arr.T - np.diag(arr.diagonal())
def symarray(arr):
    return symmetrize(np.asarray(arr)).view(symNDarray)


# get indeces of lines of interest on fchk file
def get_index(ifile,dtype):
    flags={}
    with open(ifile+'.fchk') as fo:
        forceF=0
        if dtype != 'scf' and dtype != 'ci':
            print 'Error! Density type not recognized.\nTerminating program.'
            sys.exit()
        elif dtype == 'scf' or dtype == 'ci':
            for num, line in enumerate(fo, 1):
                if 'Number of basis functions' in line:
                    flags.update({'nbasis':num})
                elif 'Nuclear charges' in line:
                    flags.update({'nuclCh':num})
                elif 'Current cartesian coordinates' in line:
                    flags.update({'cartCord':num})
                elif 'Force Field' in line: # for stop 
                    if forceF==0:
                        forceF=num
                        flags.update({'forceF':num})
                elif 'Shell types' in line:
                    flags.update({'shellType':num})
                elif 'Number of primitives per shell' in line:
                    flags.update({'shellNum':num})
                elif 'Shell to atom map' in line:
                    flags.update({'shellMap':num})
                elif 'Primitive exponents' in line:
                    flags.update({'primExp':num})
                elif 'Contraction coefficients' in line and 'P(S=P)' not in line:
                    flags.update({'contrCoeff':num})
                elif 'P(S=P) Contraction coefficients' in line:  # only present if sp orbitals
                    flags.update({'contrPSPcoeff':num})
                elif 'Coordinates of each shell' in line:
                    flags.update({'shellCord':num})
                elif 'Constraint Structure' in line: # for stop
                    flags.update({'constrStruc':num})
                elif 'Alpha Orbital Energies' in line:
                    flags.update({'aMOenerg':num})
                elif 'Alpha MO coefficients' in line:
                    flags.update({'aMOcoeff':num})
                elif 'Total SCF Density' in line:
                    flags.update({'rhoSCF':num})
                elif 'Total CI Rho(1) Density' in line:
                    flags.update({'rhoCI':num})
                elif 'Mulliken Charges' in line: # for stop scf or ci
                    flags.update({'mullik':num})
            return flags


# make xyz file from input fchk file 
# user should expand dictionary at convenience
def make_xyz(ifile,indx):
    elem={'1':'H',\
          '6':'C','7':'N','8':'O','9':'F',\
          '15':'P','16':'S','17':'Cl',\
          '22':'Ti','26':'Fe','27':'Co','28':'Ni','29':'Cu','30':'Zn','35':'Br',\
          '44':'Ru','53':'I'}
    angs=0.529177249
    nucl=[]
    clst=[]
    for key in indx:
        if key == 'nuclCh':
            a=indx[key] 
        elif key == 'cartCord':
            b=indx[key] 
        elif key == 'forceF':
            c=indx[key] 
    with open(ifile+'.fchk') as lines:
        for line in islice(lines,a,b-1):
            buff=line.strip('\n')
            buff=buff.split()
            for i in range(len(buff)):
                buff[i]=str(int(float(buff[i])))
            for key in elem:
                for i in range(len(buff)):
                    buff[i] = buff[i].replace(key,elem[key])
            for i in range(len(buff)):
                nucl.append(buff[i])
    with open(ifile+'.fchk') as lines:
        for line in islice(lines,b,c-1):
            buff=line.strip('\n')
            buff=buff.split()
            for i in range(len(buff)):
                clst.append(float(buff[i])*angs)
    if len(clst) != 3*len(nucl):
        print 'Error! Number of coordinates doesn\'t match number of atoms.\nTerminating program.' 
        sys.exit()
    ofile=open(ifile+'.in.xyz','w')
    ofile.write(str(len(nucl))+'\n'+ifile+'\n')
    i=0
    for j in range(0,len(clst),3):
        clst[j]="{0:.10f}".format(float(clst[j]))
        clst[j+1]="{0:.10f}".format(float(clst[j+1]))
        clst[j+2]="{0:.10f}".format(float(clst[j+2]))
        buff=str(nucl[i])+'          '+str(clst[j])+'    '+str(clst[j+1])+'    '+str(clst[j+2])+'\n'
        ofile.write(buff)
        i+=1
    ofile.close()
    return


# current work 1
# construct GTOs
def make_GTOs():


# current work 2
# get SCF density matrix
def get_rhoSCF(ifile,indx):
    rhoSCF=[]
    for key in indx:
        if key == 'rhoSCF':
            a=indx[key] 
        elif key == 'mullik':
            b=indx[key] 
        elif key == 'nbasis':
            nb=indx[key] 
    with open(ifile+'.fchk') as lines:
        for line in islice(lines,nb-1,nb):
            buff=line.strip('\n')
            buff=buff.split()
            buff=buff[-1]
            nb=buff
    with open(ifile+'.fchk') as lines:
        for line in islice(lines,a,b-1):
            buff=line.strip('\n')
            buff=buff.split()
            for i in range(len(buff)):
                buff[i]="{0:.10f}".format(float(buff[i]))
                rhoSCF.append(buff[i])
# !!!need to change from 1D to 2D array 
    return rhoSCF


# get CI density matrix
def get_rhoCI(dname,indx):
    for key in indx:
        if key == 'rhoCI':
            a=indx[key] 
        elif key == 'mullik':
            b=indx[key] 


# run program
def main():
    a=get_index(dname,dtype)
    make_xyz(dname,a)
    if dtype == 'scf':
        rhoSCF=get_rhoSCF(dname,a)
        print rhoSCF
    elif dtype == 'ci':
        get_rhoCI(dname,a)

    #b = symarray(np.zeros((3, 3)))
    #b[2,0]=42
    #b[1,2]=5
    #b[0,0]=33
    #print b 

main()

