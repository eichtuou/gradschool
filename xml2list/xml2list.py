'''
Author: Jessica M. Gonzalez-Delgado
        North Carolina State University

This script converts an NMR peak list file generated by TopSpin [XML]
to a peak list file to be read by NMRFAM-Sparky [LIST].

Run as: python xml2list.py file.xml
'''

#!/usr/bin/python
import sys


# check input file
def check():
    if len(sys.argv) == 0:
        print "Error! No XML file specified."
        print "Exiting now..."
        sys.exit()

    if sys.argv[1][-3:] != "xml": 
        print "Error! File is not XML format."
        print "Exiting now..."
        sys.exit()

    xfile = sys.argv[1]

    return xfile


# get peak information from LIST file
def getpeakinfo(xfile):
    peaks = []
    with open(xfile) as fo:
        for line in fo:
            line = line.strip()
            if len(line) == 0:
                continue
            else:
                line = line.split()
                if line[0] == "<Peak2D": 
                    peaks.append(line)
    return peaks


# write LIST file
def makelistfile(xfile,peaks):
    lfile = "out.list"
    fo = open(lfile,'w')
    fo.write("Assignment    w1    w2    Data Height\n")
    for i in range(0,len(peaks)):
        buff = peaks[i][3].replace('"','')[11:]+"    "+peaks[i][1].replace('"','')[3:]+"    "+peaks[i][2].replace('"','')[3:]+"    "+peaks[i][4].replace('"','')[10:]+"\n"
        fo.write(buff) 
    fo.close()


# MAIN PROGRAM
def main():
    infile=check()
    makelistfile(infile,getpeakinfo(infile))


# RUN PROGRAM
main()

