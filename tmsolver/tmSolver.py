#!/usr/bin/python
'''
Author: Jessica M. Gonzalez-Delgado
        North Carolina State University

This script solves the protein correlation time tau_m (tm) from the Model-Free
Analysis (MFA). It uses two spectral density functions (J), one of them includes
slow and/or fast motions, while the another one does not include those motions. 

Run as: python tmsolver.py j0.dat 

Here are the spectral density functions solved for tm using J(0):

    Spectral density function without slow or fast motions
    Equation (2) from DOI:10.1007/s10858-007-9214-2
    In terms of tm using J(0):
        [ -0.4*S2 ] * tm^3
        [ J - 1.2*S2*te - 0.4*te ] * tm^2
        [ 2*J*te - 0.4*te^2 ] * tm
        [ J*te^2 ]

    Spectral density function with slow or fast motions
    Equation (3) from DOI:10.1007/s10858-007-9214-2
    In terms of tm using J(0):
        [ -0.4*S ] * tm^5
        [ J - 1.2*S*ts - 0.4*Sf*ts - 0.4*tf - 0.8*S*tf + 0.4*Sf*tf ] * tm^4
        [ 2*J*ts - 0.8*S*ts^2 + 0.4*Sf*ts^2 + 2*J*tf - 0.4*tf^2 - 0.4*S*tf^2 + 0.4*Sf*tf^2 - 0.8*ts*tf - 1.6*S*ts*tf + 1.6*Sf*ts*tf ] * tm^3
        [ J*ts^2 + J*tf^2 + 4*J*ts*tf - 0.4*ts^2*tf - 1.6*S*ts^2*tf + 1.2*Sf*ts^2*tf - 0.8*ts*tf^2 - 1.2*S*ts*tf^2 + 1.2*Sf*ts*tf^2 ] * tm^2
        [ 2*J*ts*tf^2 + 2*J*ts^2*tf - 0.4*ts^2*tf^2 - 0.8*S*ts^2*tf^2 + 0.8*Sf*ts^2*tf^2 ] * tm 
        [ J*ts^2*tf^2 ]

'''

import numpy as np
import sys


# check input file
def check():
    if len(sys.argv) == 0:
        print "Error! No DAT file specified."
        print "Exiting now..."
        sys.exit()

    if sys.argv[1][-3:] != "dat": 
        print "Error! File is not DAT format."
        print "Exiting now..."
        sys.exit()

    dfile = sys.argv[1]

    return dfile


# get MFA data for each residue
def getmfadata(dfile):
    resid = []
    j_vals = []
    s_vals = []
    sf_vals = []
    ss_vals = []
    te_vals = []
    tf_vals = []
    ts_vals = []

    with open(dfile) as fo:
        for line in fo:
            line = line.strip().split()
            if '#' in line[0] :
                continue
            resid.append(int(line[0]))
            j_vals.append(float(line[1]))
            s_vals.append(float(line[2]))
            sf_vals.append(float(line[3]))
            ss_vals.append(float(line[4]))
            te_vals.append(float(line[5]))
            tf_vals.append(float(line[6]))
            ts_vals.append(float(line[7]))

    return resid,j_vals,s_vals,sf_vals,ss_vals,te_vals,tf_vals,ts_vals 


# calculate tm values from first density function
def tm_1(dfile,mfa):
    tm = 0
    tm_vals = []

    fo = open(dfile[:-4]+'-tm.dat','w')
    fo.write("tm values [s] (without slow or fast motions)\n")

    for i in range(0,len(mfa[0])):
        res = mfa[0][i]
        j = mfa[1][i]
        s = mfa[2][i]
        sf = mfa[3][i]
        ss = mfa[4][i]
        te = mfa[5][i]
        tf = mfa[6][i]
        ts = mfa[7][i]
        
        a = -0.4*s
        b = j - 1.2*s*te - 0.4*te 
        c = 2.0*j*te - 0.4*te**2 
        d = j*te**2 
    
        tm = np.roots([a,b,c,d])

        if tm.size == 0 or tm[0] == 0:
            tm = "None"
        else:
            tm = tm[0]
            tm_vals.append(tm)
    
        buff = "residue "+str(res)+" = "+str(tm)+'\n'
        fo.write(buff)

        if i == len(mfa[0])-1:
            buff = "Average tm [s] = "+str(np.average(tm_vals))+'\n'
            fo.write(buff)
            buff = "Std dev tm [s] = "+str(np.std(tm_vals))+'\n'
            fo.write(buff)

    fo.close()


# tm values from second density function
def tm_2(dfile,mfa): 
    tm = 0
    tm_vals = []
                                                               
    fo = open(dfile[:-4]+'-tm.dat','a')
    fo.write("\ntm values [s] (with slow or fast motions)\n")
    
    for i in range(0,len(mfa[0])):
        res = mfa[0][i]
        j = mfa[1][i]
        s = mfa[2][i]
        sf = mfa[3][i]
        ss = mfa[4][i]
        te = mfa[5][i]
        tf = mfa[6][i]
        ts = mfa[7][i]

        a =  -0.4*s
        b =  j - 1.2*s*ts - 0.4*sf*ts - 0.4*tf - 0.8*s*tf + 0.4*sf*tf
        c =  2.0*j*ts - 0.8*s*(ts**2) + 0.4*sf*(ts**2) + 2*j*tf - 0.4*(tf**2) - 0.4*s*(tf**2) + 0.4*sf*(tf**2) - 0.8*ts*tf - 1.6*s*ts*tf + 1.6*sf*ts*tf
        d =  j*(ts**2) + j*(tf**2) + 4*j*ts*tf - 0.4*(ts**2)*tf - 1.6*s*(ts**2)*tf + 1.2*sf*(ts**2)*tf - 0.8*ts*(tf**2) - 1.2*s*ts*(tf**2) + 1.2*sf*ts*(tf**2)
        e =  2*j*ts*(tf**2) + 2*j*(ts**2)*tf - 0.4*(ts**2)*(tf**2) - 0.8*s*(ts**2)*(tf**2) + 0.8*sf*(ts**2)*(tf**2)
        f =  j*(ts**2)*(tf**2) 
    
        tm = np.roots([a,b,c,d,e,f])
        if tm.size == 0 or tm[0] == 0:
            tm = "None"
        else:
            tm=tm[0]
            tm_vals.append(tm)

        buff = "residue "+str(res)+" = "+str(tm)+'\n'
        fo.write(buff)
                                                                     
        if i == len(mfa[0])-1:
            buff = "Average tm [s] = "+str(np.average(tm_vals))+'\n'
            fo.write(buff)
            buff = "Std dev tm [s] = "+str(np.std(tm_vals))+'\n'
            fo.write(buff)

    fo.close()


# MAIN PROGRAM
def main():
    datfile = check()
    mfa = getmfadata(datfile)
    tm_1(datfile,mfa)
    tm_2(datfile,mfa)



# RUN PROGRAM
main()

