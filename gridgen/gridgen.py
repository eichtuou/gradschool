#!/usr/bin/python
'''
Author: Jessica M. Gonzalez-Delgado
	North Carolina State University

This script reads an molecular structure [XYZ] file and creates a box around the 
system with a user specified "padding" in units of Angstroms. The box is then
partitioned into smaller boxes [inp_cube_*.dat], which are then utilized as part 
of the input needed for performing parallel denstity calculations in the whole 
system in Gaussian09.

Run as: python gridgen.py file.xyz
'''

#-------------------- USER INPUT SECTION --------------------!
xpad=2.0             # padding in x direction [angs]
ypad=2.0             # padding in y direction [angs]
zpad=2.0             # padding in z direction [angs]
nx=4                 # has to be n+1, n = cubes in x direction
ny=4                 # has to be n+1, n = cubes in y direction
nz=4                 # has to be n+1, n = cubes in z direction
xpts=175             # points in x direction (resolution) 
ypts=175             # points in y direction (resolution) 
zpts=175             # points in z direction (resolution) 
#------------------------------------------------------------!

import sys
import numpy as np
from itertools import product


# check 
def check():
    if len(sys.argv[1]) == 0:
        print "Error! No XYZ file specified."
        print "Exiting now..."
        sys.exit()

    if sys.argv[1][-4:] != ".xyz": 
        print "Error! File is not XYZ format."
        print "Exiting now..."
        sys.exit()

    if xpad < 0 or ypad < 0 or zpad < 0:
        print "Error! Padding cannot be less than 0 Angstroms."
        print "Exiting now..."
        sys.exit()

    if nx < 1 or ny < 1 or nz < 1: 
        print "Error! That cube partition is not possible."
        print "Exiting now..."
        sys.exit()

    if xpts < 1 or ypts < 1 or zpts < 1: 
        print "Error! That resolution is not possible."
        print "Exiting now..."
        sys.exit()

    xyzfile=sys.argv[1]
    
    return xyzfile


# get xyz coordinates
def get_xyz(xyzfile):
    xcords = []
    ycords = []
    zcords = []

    with open(xyzfile) as fo:
        lines = fo.readlines()
        lines = lines[2:]

        for line in lines:
            line = line.strip('\n').split()
            xcords.append(float(line[1]))
            ycords.append(float(line[2]))
            zcords.append(float(line[3]))

    return xcords,ycords,zcords


# create box with padding
def make_box(x,y,z,xpad,ypad,zpad):
    origin = []
    maxcords = []

    origin.append(min(x)-xpad)
    origin.append(min(y)-ypad)
    origin.append(min(z)-zpad)

    maxcords.append(max(x)+xpad)
    maxcords.append(max(y)+ypad)
    maxcords.append(max(z)+zpad)

    return origin,maxcords


# split box
def split_box(mincords,maxcords,nx,ny,nz):
    # get dimensions
    xdim = float(format(float(maxcords[0]-mincords[0]),'.9f'))
    ydim = float(format(float(maxcords[1]-mincords[1]),'.9f'))
    zdim = float(format(float(maxcords[2]-mincords[2]),'.9f'))

    # step size
    # needed for input streams
    dx = (xdim/(nx-1))
    dy = (ydim/(ny-1))
    dz = (zdim/(nz-1))

    # list of coordinates for smaller boxes 
    # needed for input streams 
    xgrid = np.delete(np.linspace(mincords[0],maxcords[0],nx),nx-1)
    ygrid = np.delete(np.linspace(mincords[1],maxcords[1],ny),ny-1)
    zgrid = np.delete(np.linspace(mincords[2],maxcords[2],nz),nz-1)

    return dx,dy,dz,list(product(xgrid,ygrid,zgrid))


# create input streams for calculation submissions
def make_instreams(nx,ny,nz,xpts,ypts,zpts,dx,dy,dz,cords):
    # total number of cubes
    tcubes = (nx-1)*(ny-1)*(nz-1)

    # quick check
    if tcubes != len(cords):
        print "Something went wrong."
        print "Exiting now..."
        sys.exit()

    # clean coordinates
    for i in range(0,len(cords)):
        buff = str(cords[i]).strip('()')
        buff = buff.replace(',','')
        cords[i] = buff

    # adjust resolution --> steps/points
    rsln = []
    dx = format(float(dx/xpts),'.9f')
    dy = format(float(dy/ypts),'.9f')
    dz = format(float(dz/zpts),'.9f')
    zeros = '0.000000000'
    rsln.append(str(xpts)+', '+dx+', '+zeros+', '+zeros)
    rsln.append(str(ypts)+', '+zeros+', '+dy+', '+zeros)
    rsln.append(str(zpts)+', '+zeros+', '+zeros+', '+dz)

    # make input streams 
    for i in range(1,tcubes+1):
        instream_file = 'inp_cube_'+str(i)+'.dat'
        buff = cords[i-1].split()
        buff[0] = format(float(buff[0]),'.9f')
        buff[1] = format(float(buff[1]),'.9f')
        buff[2] = format(float(buff[2]),'.9f')
        header = '-1, '+buff[0]+', '+buff[1]+', '+buff[2]+'\n'
        fo = open(instream_file,'w') 
        fo.write(header)
        for j in range(3):
            buff2 = rsln[j].strip()+'\n'
            fo.write(buff2)
        fo.close()


# MAIN PROGRAM
def main():
    xyz = get_xyz(check())
    box = make_box(xyz[0],xyz[1],xyz[2],xpad,ypad,zpad)
    boxes = split_box(box[0],box[1],nx,ny,nz)
    make_instreams(nx,ny,nz,xpts,ypts,zpts,boxes[0],boxes[1],boxes[2],boxes[3])



# RUN PROGRAM
main()

