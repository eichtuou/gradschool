'''
Author: Jessica M. Gonzalez-Delgado
        North Carolina State University

This script baseline corrects and removes cosmic rays from various 
raman spectra files of the same sample, and it also generates an 
averaged corrected spectrum. All spectra files are also corrected
with the toluene reference spectrum. 

Spectra to be corrected should be located in a single directory.

To baseline correct the spectra, the baseline correction points 
must be provided in the "USER INPUT" section.

To correct the spectra with the toluene reference spectrum, the
pixel numbers of the five reference peaks must be provided in the
"USER INPUT" section.

Run as: python rmCosmics.py
'''

#--------------------- USER INPUT ---------------------#
# baseline correction points
bcpts=[20,42,159,208,241,368,463,546,666,710,734,826,1029,1121,1176,1225,1250,1291,1316,1332]
# pixel numbers of toluene reference peaks 
tolpix=[108.94,147.46,387.70,618.52,931.40]
#------------------------------------------------------#

import os
import sys
import numpy as np

# get spectra files 
def getSpecs(afiles):
    specs=[]
    for afile in afiles:
        if afile[-4:] == ".txt":
            specs.append(afile)
    return specs

# get number of pixels and create data array 
def getPix(sfiles):
    pix=sum(1 for line in open(sfiles[0]))
    # one extra column for average values
    data=np.zeros(shape=(pix,len(sfiles)+1))
    return pix,data


# read spectra files and fill data array 
def getData(sfiles,pix,data):
    j=0
    for sfile in sfiles:
        with open(sfile,'r') as fo:
            lines=fo.readlines()
        lines=[line.strip().split(',')[-1] for line in lines]
        for i in range(0,pix):
            data[i][j]=lines[i]
        j+=1
    return data


# baseline correct data
def blcor(sfiles,zpts,data):
    # get fraction of baseline from zeros provided by user
    bl=np.zeros(shape=(len(zpts),len(sfiles)))
    for i in range(0,len(zpts)):
        for j in range(0,len(sfiles)):
            bl[i][j]=data[zpts[i]][j]
    # actual baseline interpolated from previous baseline fraction
    for i in range(0,len(sfiles)):	
        abl=np.interp(np.arange(1,len(data)+1),zpts,bl[:,i].tolist())
        # substract baseline
        for j in range(0,len(data)):
            data[j][i]=data[j][i]-abl[j]
    return data


#create copies of baseline corrected spectra files
def mkcp(sfiles,data):
    for i in range(0,len(sfiles)):
        with open(sfiles[i][:-4]+'-bc.dat','w') as fo:
            for j in range(0,len(data)):
                buff=str(j+1)+'    '+str(data[j][i])
                fo.write(buff+'\n')

# remove cosmic rays 
def delCosmics(sfiles,data):
    for i in range(0,len(data)):
        avg=np.mean(data[i,:-1])
        stdp=np.std(data[i,:-1])
        data[i][-1]=avg
        for j in range(0,len(sfiles)):
            if data[i][j] >= avg+stdp:
                data[i][j]=avg
    return data


# get correction for toluene spectrum
def getCor4tol(tpix):
    x=np.array(tpix)
    y=np.array([1003.1,1030.1,1210.0,1378.6,1604.1])
    a=np.vstack([x,np.ones(len(x))]).T
    m,c=np.linalg.lstsq(a,y,rcond=None)[0]
    return m,c


# write new files
def makeSpecs(sfiles,data,tcor):
    # convert pixels into wavenumbers
    pix=[x for x in range(1,len(data)+1)]
    xw=tcor[0]
    yi=tcor[1]
    for i in range(1,len(data)+1):
        pix[i-1]=pix[i-1]*xw+yi
    # corrected spectra files
    for sfile in sfiles:
        nwspec=sfile[:-4]+'-rmc.dat'
        with open(nwspec,'w') as fo:
            for i in range(0,len(pix)):
                buff=str(pix[i])+'    '+(str(data[i][sfiles.index(sfile)]))
                fo.write(buff+'\n')
    # averaged corrected spectrum
    avgspec='avg-bc-rmc-spec.dat' 
    with open(avgspec,'w') as fo:
        for i in range(0,len(pix)):
            buff=str(pix[i])+'    '+(str(data[i][-1]))
            fo.write(buff+'\n')


# MAIN PROGRAM
def main(zpts):
    dirfiles=os.listdir(os.getcwd())
    specs=getSpecs(dirfiles)
    pixdat=getPix(specs)
    data=getData(specs,pixdat[0],pixdat[1])
    mkcp(specs,blcor(specs,zpts,data))
    cordat=delCosmics(specs,blcor(specs,zpts,data))
    makeSpecs(specs,cordat,getCor4tol(tolpix))



# RUN PROGRAM
main(bcpts)

