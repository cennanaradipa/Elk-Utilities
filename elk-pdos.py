#! /usr/bin/env python

# Invoke with column nr to extract as first parameter followed by
#   filenames. The files should all have the same number of rows

# Input can be any combination of PDOS files, even other output 
# Output = gnuplot format with 16 datasets (based on ELMIREP)
#   and each column represents a atom N for each species (filename)
# Can also be used to get total PDOS for each atoms
#   or any other combination of files

# Author : Muhammad Avicenna Naradipa
# Modified version of blocks2columns 

# Usage: elk-pdos.py PDOS_S01_A000*
#        elk-pdos.py PDOS_S0*

# Plotting in gnuplot :
#   plot for [index=0:ndatasets] "outfile" i index u 1:2 with lines
# Columns are different list of all files combined + total of these files
#   i.e. can show different components of atoms, u 1:2,3,4,..no of filenames
# Band information (ELMIREP) can be set by plotting certain datasets
#   i.e. for plotting p-bands (l = 1) set [index=1:3]

import sys
import os

print("\n =========================\n | Elk PDOS Combiner  |\n =========================\n")

# Read the files.
filenames = []
for i in sys.argv[1:]:
    filenames.append(i)

# Finding datasets, lines/block, etc.
# Taken from blocks2columns
ndatasets = 0
nlinesperblock = 0
f = open(filenames[0],'r')
print "\nExtracting x-axis data from " + filenames[0]
current = f.readlines()
nlines = len(current)
f.close

for line in current:
    if line.split() == []:
        ndatasets += 1
if current[-1].split() != []:
    ndatasets += 1
    nlines += 1
print("Number of datasets: %i " % ndatasets)

nlinesperblock = (nlines - ndatasets)/ndatasets
print("Number of lines per block: %i " % nlinesperblock)


# Additional feature for setting custom species name
print "\nWould you like to rename the output files?"
print "Useful when combining only a certain species."
print "Default name is \'pdos_combo.dat\'"
species = raw_input("\nIf so, enter the name here :\n")
if species is None:
    outfile = "pdos_combo.dat"
else:
    outfile = "pdos_" + species + ".dat"

# Datasets are now in a list^3 as we need to address the file types.
# fulldata = [filesets][ndatasets][linesperblock][first col/second col]
fulldata = []
for i in range(0,len(filenames)):
    filesets = []
    f = open(filenames[i],'r')
    currentfile = f.readlines()
    print "Extracting y-axis from " + filenames[i] 
    for j in range(0,ndatasets):
        currentset = []
        for k in range(j*nlinesperblock + j, (j*nlinesperblock + j) + nlinesperblock):
        #for k in range(0,nlinesperblock):
            currentset.append(currentfile[k].split())
        filesets.append(currentset)
    fulldata.append(filesets)
    f.close()


# Generate Header for each filename
output = ""
output += "#%21s" % "Energy (Ha)"
for i in range(0,len(filenames)):
    output += "%22s" % filenames[i]
output += "%22s" % "Total PDOS"
output += "\n"

# Outputs will be separted by new lines with captions in quotes
# This is to support gnuplot columnheader
# TODO: Port ELMIREP's data to the header
# TODO: Be able to differentiate between datasets from ELMIREP
#       and different spins in spinpol calculations
# Plot all datasets in one column, but separated by newline

for i in range(0,ndatasets):
    output += '\n\"dataset %s\"\n' % str(i+1) 
    line = ''
    for j in range(0,nlinesperblock):
        line += '%22.8f' % (float(fulldata[0][0][j][0]))

        total_pdos = 0
        for k in range (0, len(filenames)):
            line += '%22.8f' % (float(fulldata[k][i][j][1]))
            total_pdos += float(fulldata[k][i][j][1])
        line += '%22.8f' % float(total_pdos)
        line += "\n"
    line += "\n"
    output += line


# Also from blocks2columns
if os.path.exists(outfile):
    print("\nOutput file %s exists. Exit.\n" % outfile)
else:
    f = open(outfile, 'w')
    f.write(output)
    f.close()   
    print("\nOutput filename: %s\n Done.\n" % outfile)
