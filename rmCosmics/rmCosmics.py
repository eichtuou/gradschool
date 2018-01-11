'''
This script reads removes cosmic rays from various raman spectra files of
the same sample, and also generates an averaged corrected spectrum. 

Spectra to be corrected should be located in a single directory. If there
are any dead pixels, they should be added to "deadpix" list. 

Run as: python rmCosmics.py
'''

# dead pixels to be removed
deadpix=[891]

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


# get number of pixels 
def getPix(sfiles):
	pix=sum(1 for line in open(sfiles[0]))
	data=np.zeros(shape=(pix,len(sfiles)+1))
	return pix,data


# read spectra files 
def getData(sfiles,pix,data):
	j=0
	for sfile in sfiles:
		with open(sfile,'r') as fo:
			lines=fo.readlines()
		# get data and append to 1d arrays
		lines=[line.strip().split(',')[-1] for line in lines]
		for i in range(0,pix):
			data[i][j]=lines[i]
		j+=1
	return data


# remove cosmic rays 
def delCosmics(sfiles,pix,data):
	for i in range(0,pix):
		avg=np.mean(data[i,:])
		stdp=np.std(data[i,:])
		data[i][-1]=avg
		for j in range(0,len(sfiles)):
			if data[i][j] >= avg+2*stdp:
				data[i][j]=avg
	return data


# write new files
def makeSpecs(sfiles,pix,dpix,data):
	for sfile in sfiles:
		nwspec=sfile[:-4]+'_cor.txt'
		with open(nwspec,'w') as fo:
			for i in range(1,pix+1):
				if i in dpix:
					continue 
				buff=str(i)+','+(str(data[i-1][sfiles.index(sfile)]))
				fo.write(buff+'\n')

	avgspec='avg_spec.txt' 
	with open(avgspec,'w') as fo:
		for i in range(1,pix+1):
			if i in dpix:
				continue
			buff=str(i)+','+(str(data[i-1][-1]))
			fo.write(buff+'\n')


# MAIN PROGRAM
def main(dpix):
	dirfiles=os.listdir(os.getcwd())
	specs=getSpecs(dirfiles)
	pixdat=getPix(specs)
	cordat=delCosmics(specs,pixdat[0],getData(specs,pixdat[0],pixdat[1]))
	makeSpecs(specs,pixdat[0],dpix,cordat)



# RUN PROGRAM
main(deadpix)

