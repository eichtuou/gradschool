'''
Author: Jessica M. Gonzalez-Delgado
		North Carolina State University

This script performs a cubic interpolation of raman spectra and 
generates a new spectrum file with a new x-range and averaged
y-values. To use this script, have only normalized and baseline 
corrected spectra of one sample to be averaged in a single 
directory. 

Run as: python spline-avg.py xinitial xfinal 
'''

import os
import sys
import numpy as np
import scipy as sp
from scipy.interpolate import interp1d

# get spectrum files 
def getSpecs(afiles):
	specs=[]
	twice = False
	for afile in afiles:
		if "-sc-sp.txt" in afile:
			twice = True
			specs.append(afile)
		if twice == False and "-sc.txt" in afile:
			specs.append(afile)
	return specs	


# make cubic interpolation 
def makeCI(sfiles,xi,xf):
	for sfile in sfiles:
		# read spectrum
		with open(sfile,'r') as fo:
			lines=fo.readlines()
		lines=[line.strip().split() for line in lines]
		# get x and y values from spectrum
		x=[]
		y=[]
		for i in range(0,len(lines)):
			x.append(float(lines[i][0]))
			y.append(float(lines[i][1]))
		x=np.array(x)
		y=np.array(y)
		# perform cubic interpolation
		xnew=np.linspace(xi,xf,len(lines))
		ynew=sp.interpolate.interp1d(x,y,kind='cubic')(xnew)
		xnew=xnew.tolist()
		ynew=ynew.tolist()
		# write new spectrum files	
		makeFile(sfile,xnew,ynew,'sp')


# create data array 
def makeDarr(sfiles):
	xlen=sum(1 for line in open(sfiles[0]))
	# add two extra columns for x-values and average 
	data=np.zeros(shape=(xlen,len(sfiles)+2))
	# read x-values from first spectrum and write in
	# first column of array
	with open(sfiles[0],'r') as fo:
		lines=fo.readlines()
	lines=[line.strip().split() for line in lines]
	for i in range(0,len(lines)):
		data[i][0]=lines[i][0]
	return data


# fill data array 
def getData(sfiles,data):
	j=1
	for sfile in sfiles:
		with open(sfile,'r') as fo:
			lines=fo.readlines()
		lines=[line.strip().split()[-1] for line in lines]
		for i in range(0,len(data)):
			data[i][j]=lines[i]
		j+=1
	return data


# average interpolated spectra and remove cosmic rays 
def makeAvg(sfiles,data):
	# average y-values
	for i in range(0,len(data)):
		avg=np.mean(data[i,1:-1])
		stdp=np.std(data[i,1:-1])
		data[i][-1]=avg
		# remove cosmic rays
		for j in range(1,len(sfiles)):
			if data[i][j] >= avg+stdp:
				data[i][j]=avg
	# write averaged spectrum file
	outfile='avg_spec.txt' 
	with open(outfile,'w') as fo:
		for i in range(0,len(data)):
			buff=str(data[i][0])+'    '+(str(data[i][-1]))
			fo.write(buff+'\n')
	# write corrected files
	i=1
	for sfile in sfiles:
		makeFile(sfile,data[:,0],data[:,i],'cor')
		i+=1

# write new files	
def makeFile(sfile,x,y,t):
	with open(sfile[:-4]+'-'+t+'.txt','w') as fo:
		for i in range(0,len(x)):
			buff=str(x[i])+'    '+str(y[i])+'\n'
			fo.write(buff)


# MAIN PROGRAM
def main(xi,xf):
	specs=getSpecs(os.listdir(os.getcwd()))
 	xvals=makeCI(specs,xi,xf)
	specs=getSpecs(os.listdir(os.getcwd()))
	data=makeDarr(specs)
	data=getData(specs,data)
	makeAvg(specs,data)


# RUN PROGRAM
main(int(sys.argv[1]),int(sys.argv[2]))

