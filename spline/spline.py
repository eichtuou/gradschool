'''
Author: Jessica M. Gonzalez-Delgado
		North Carolina State University

This script performs a cubic interpolation of a raman spectrum 
and generates a new spectrum file with a new x-range. This is
useful when different spectra of the same sample have different
calibrations and cannot be averaged. Using this script will let 
the user average these spectra. 

Run as: python spline.py file.txt
'''

import sys
import numpy as np
import scipy as sp
from scipy.interpolate import interp1d

spec=sys.argv[1]

with open(spec,'r') as fo:
	lines=fo.readlines()
lines=[line.strip().split() for line in lines]

x=[]
y=[]

for i in range(0,len(lines)):
	x.append(float(lines[i][0]))
	y.append(float(lines[i][1]))

x=np.array(x)
y=np.array(y)

xnew=np.linspace(900,1800,len(lines))
ynew=sp.interpolate.interp1d(x,y,kind='cubic')(xnew)

xnew=xnew.tolist()
ynew=ynew.tolist()

with open(spec[:-4]+'-sp.txt','w') as fo:
	for i in range(0,len(lines)):
		buff=str(xnew[i])+'    '+str(ynew[i])+'\n'
		fo.write(buff)

