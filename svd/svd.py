'''
Author: Jessica M. Gonzalez-Delgado
	North Carolina State University

This script performs SVD analysis on a CSV data file of the following format:
    # comment 
    # comment 
    ,x1,y1,y2,y3,y4,...,yn,
    x2,y1,y2,y3,y4,...,yn,
    # maybe a comment here
    ...
    xn,y1,y2,y3,y4,...,yn,

(1) lines starting with # are considered comments and are ignored.
(2) first column corresponds to the "x-axis" and is ignored when building the 
    data matrix.
(3) if there is a comma at the beginning or ending of a line, it will be 
    corrected.

The scripts outputs a CSV file containing the VT matrix components labeled as:
    data-vt.csv 

run as: python svd.py data.csv

'''

#!/usr/bin/python
import sys
import numpy as np


# check input file
def check():
    if len(sys.argv) == 0:
        print "Error! No CSV file specified."
        print "Exiting now..."
        sys.exit()

    if sys.argv[1][-3:] != "csv": 
        print "Error! File is not CSV format."
        print "Exiting now..."
        sys.exit()

    dfile = sys.argv[1]

    return dfile


# get data from CSV file
def getData(dfile):
    data = []
    with open(dfile) as fo:
        for line in fo:
            line = line.rstrip()
            # ignore comment lines
            if line[0] != '#':
                line = line.split(',')
                # trim first and last commas if present
                if len(line[0]) == 0:
                    line = line[1:]
                if len(line[-1]) == 0:
                    line = line[:-1]
                # ignore x-values in first column, data array only has y-values 
                line = line[1:]
                # convert from string to float and fill data array
                for i in range(0,len(line)):
                    line[i] = float(line[i])
                data.append(line)
    data = np.array(data)

    return data


# perform SVD analysis and write the VT matrix components in a file
def doSVD(dfile,darr):
    u,s,vt = np.linalg.svd(darr)
    
    # save VT components in a CSV file
    ofile = dfile[:-4]+"-vt.csv"
    fo = open(ofile, 'w')
    for i in range(0,len(vt)):
        buff = "VT component #"+str(i+1)+" " 
        for j in range(0,len(vt)):
            if j == len(vt)-1:
                buff = buff + str(vt[i][j])+"\n"
            else:
                buff = buff + str(vt[i][j])+", "
        fo.write(buff)
    fo.close()


# MAIN PROGRAM
def main():
    infile = check()
    data = getData(infile)
    doSVD(infile,data)



# RUN PROGRAM
main()

