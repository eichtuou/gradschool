'''
Author: Jessica M. Gonzalez-Delgado
        North Carolina State University

This script performs a cubic interpolation of raman spectra and 
generates a new spectrum file with a new x-range and averaged
y-values. To use this script, have only normalized and baseline
corrected spectra of one sample to be averaged in a single directory. 

Run as: python spline-avg.py xinitial xfinal 
'''

#!/usr/bin/python
import os
import sys
import numpy as np
import scipy as sp
from scipy.interpolate import interp1d


# check input arguments
def check():
    if len(sys.argv) > 3:
        print "Error! Must specify only two x-range values."
        print "Exiting now..."
        sys.exit()
    if len(sys.argv) == 1:
        print "Error! No x-range specified."
        print "Exiting now..."
        sys.exit()
    if len(sys.argv) == 2:
        print "Error! Missing x-range value."
        print "Exiting now..."
        sys.exit()


# get spectrum files 
def getSpecs(afiles):
    specs = []
    for afile in afiles:
        if afile[-4:] == ".dat":
            specs.append(afile)
    return specs


# make cubic interpolation 
def makeCI(sfiles,xi,xf):
    spfiles = []
    for sfile in sfiles:
        # read spectrum
        with open(sfile,'r') as fo:
            lines = fo.readlines()
        lines = [line.strip().split() for line in lines]
        # get x and y values from spectrum
        x = []
        y = []
        for i in range(0,len(lines)):
            x.append(float(lines[i][0]))
            y.append(float(lines[i][1]))
        x = np.array(x)
        y = np.array(y)
        # perform cubic interpolation
        xnew = np.linspace(xi,xf,len(lines))
        ynew = sp.interpolate.interp1d(x,y,kind='cubic')(xnew)
        xnew = xnew.tolist()
        ynew = ynew.tolist()
        # write new spectrum files
        makeFile(sfile,xnew,ynew,'sp')
        spfiles.append(sfile[:-4]+"-sp.dat")
    return spfiles

# create data array
def makeDarr(spfiles):
    xlen = sum(1 for line in open(spfiles[0]))

    # add two extra columns for x-values and average 
    data = np.zeros(shape=(xlen,len(spfiles)+2))

    # read x-values from first spectrum and write in
    # first column of array
    with open(spfiles[0],'r') as fo:
        lines = fo.readlines()
    lines = [line.strip().split() for line in lines]
    for i in range(0,len(lines)):
        data[i][0] = lines[i][0]
    return data


# fill data array 
def getData(spfiles,data):
    j = 1
    for spfile in spfiles:
        with open(spfile,'r') as fo:
            lines = fo.readlines()
        lines = [line.strip().split()[-1] for line in lines]
        for i in range(0,len(data)):
            data[i][j] = lines[i]
        j+=1
    return data


# average interpolated spectra
def makeAvg(data):
    # average y-values
    for i in range(0,len(data)):
        avg = np.mean(data[i,1:-1])
        stdp = np.std(data[i,1:-1])
        data[i][-1] = avg
    # write averaged spectrum file
    outfile='avg-sp-spec.dat' 
    with open(outfile,'w') as fo:
        for i in range(0,len(data)):
            buff = str(data[i][0])+'    '+(str(data[i][-1]))
            fo.write(buff+'\n')


# write new files
def makeFile(afile,x,y,t):
    with open(afile[:-4]+'-'+t+'.dat','w') as fo:
        for i in range(0,len(x)):
            buff = str(x[i])+'    '+str(y[i])+'\n'
            fo.write(buff)


# MAIN PROGRAM
def main(xi,xf):
    specs1 = getSpecs(os.listdir(os.getcwd()))
    specs2 = makeCI(specs1,xi,xf)
    data = makeDarr(specs2)
    data = getData(specs2,data)
    makeAvg(data)


# RUN PROGRAM
check()
main(int(sys.argv[1]),int(sys.argv[2]))

