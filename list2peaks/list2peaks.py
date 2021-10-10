'''
Author: Jessica M. Gonzalez-Delgado
        North Carolina State University

This script converts an NMR peak list file generated by NMRFAM-Sparky [LIST]
to a peak list file to be read by TopSpin [PEAKS].

Run as: python list2peaks.py file.list
'''

#!/usr/bin/python
import sys


# check input file
def check():
    if len(sys.argv) == 0:
        print "Error! No LIST file specified."
        print "Exiting now..."
        sys.exit()

    if sys.argv[1][-4:] != "list": 
        print "Error! File is not LIST format."
        print "Exiting now..."
        sys.exit()

    lfile = sys.argv[1]

    return lfile


# get peak information from LIST file
def getpeakinfo(lfile):
    peaks = []
    with open(lfile) as fo:
        for line in fo:
            line = line.strip()
            if len(line) == 0:
                continue
            else:
                line = line.split()
                if line[0] == "Assignment": 
                    continue
                else:
                    peaks.append(line)
    return peaks


# write PEAKS file
def makepeaksfile(lfile,peaks):
    pfile = "out.peaks"
    fo = open(pfile,'w')
    fo.write("# Number of dimensions 2\n")
    for i in range(0,len(peaks)):
        buff = str(i+1)+" "+peaks[i][1]+" "+peaks[i][2]+" 1 - 0.000E00 0.000E00 - 0 0 0 0\n#"+peaks[i][0]+"\n"
        fo.write(buff) 
    fo.close()


# MAIN PROGRAM
def main():
    infile = check()
    makepeaksfile(infile,getpeakinfo(infile))


# RUN PROGRAM
main()

