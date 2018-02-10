'''
This script baseline corrects and removes cosmic rays from various 
raman spectra files of the same sample, and it also generates an 
averaged corrected spectrum. 

Spectra to be corrected should be located in a single directory.

To baseline correct the spectra, the baseline correction points 
must be provided in the "USER INPUT" section. 

Run as: python rmCosmics.py
'''

#--------------------- USER INPUT ---------------------#
# baseline correction points
bcpts=[88,228,393,487,745,1012,1120,1265]
#------------------------------------------------------#

import os
import sys
import numpy as np

# get spectra files 
def getSpecs(afiles):
	specs=[]
	for afile in afiles:
		if ".txt" in afile:
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


# remove cosmic rays 
def delCosmics(sfiles,data):
	for i in range(0,len(data)):
		avg=np.mean(data[i,:-1])
		stdp=np.std(data[i,:-1])
		data[i][-1]=avg
		for j in range(0,len(sfiles)):
			if data[i][j] >= avg+1*stdp:
				data[i][j]=avg
	return data


# write new files
def makeSpecs(sfiles,data):
	# corrected spectra files
	for sfile in sfiles:
		nwspec=sfile[:-4]+'_cor.txt'
		with open(nwspec,'w') as fo:
			for i in range(1,len(data)+1):
				buff=str(i)+','+(str(data[i-1][sfiles.index(sfile)]))
				fo.write(buff+'\n')
	# averaged corrected spectrum
	avgspec='avg_spec.txt' 
	with open(avgspec,'w') as fo:
		for i in range(1,len(data)+1):
			buff=str(i)+','+(str(data[i-1][-1]))
			fo.write(buff+'\n')


# MAIN PROGRAM
def main(zpts):
	dirfiles=os.listdir(os.getcwd())
	specs=getSpecs(dirfiles)
	pixdat=getPix(specs)
	data=getData(specs,pixdat[0],pixdat[1])
	cordat=delCosmics(specs,blcor(specs,zpts,data))
	makeSpecs(specs,cordat)



# RUN PROGRAM
main(bcpts)

