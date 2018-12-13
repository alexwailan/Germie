
#!/usr/bin/env python3


#Created: 03.12.18 - Alexander Wailan 


import os
import sys
import pandas
import argparse
import pandas as pd
import numpy as np
import subprocess
import pathlib
from pathlib import Path
import shutil

##########################################
# Check if dependent programs are loaded #
##########################################

dependencies = [
'iqtree',
'pyjar.py'
]

print()
print("Checking dependencies mate! \n")
def depend_check(dependencies):
    all_d = []
    for d in dependencies:
        if shutil.which(d, mode=os.F_OK | os.X_OK, path=None) is not None:
            print("%s has been found!" %d)
            all_d.append('TRUE')
        elif shutil.which(d, mode=os.F_OK | os.X_OK, path=None) is None:
            print("Unable to find %s." %d)
            all_d.append('FALSE')
    return all_d

if not 'FALSE' in depend_check(dependencies):
    print("I can see all dependencies! \n")
else:
    print("\n Mate! Not all required dependencies are loaded.")
    sys.exit()



##########################################
# Function to Get command line arguments #
##########################################

def getargv():
    usage = 'germie.py [options] aln tree'
    description='Run Germie. A program to run iqtree then Joint Ancestral Reconstruction.'
    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument('aln', action="store", help='Provide the alignment file.', metavar='N',nargs='?')
    parser.add_argument('tree', action="store", help='Prefix of output JAR tree.', metavar='N', type=str, nargs='?')
    parser.add_argument('-d',    '--dirpath',  action="store",dest="pdir", help='Input directory containing alignment. End with a forward slash. Eg. /temp/fasta/', metavar='N', type=str, nargs='?', default=os.getcwd()+'/')
    parser.add_argument('-o',    '--outdir', action="store", dest="odir", help='Output directory. End with a forward slash. Eg. /temp/fasta/; Default to use current directory.', metavar='N', type=str, nargs='?', default=os.getcwd()+'/')
    return parser.parse_args()


args = getargv()

##the project directory that holds the alignment file
idir = args.pdir

##the project directory that holds the output
odir = args.odir

#reading in aln file
aln = args.aln

#reading in tree name
tree = args.tree

##where do you want the output to go

##if the project directory and output directory don't have a forward slash exit
if(idir[-1]!='/'):
  print(idir[-1])
  print('\n The project directory should end with a forward slash')
  sys.exit()

#Let your peeps know what is happening. Just a bit of communication.
print(" ")
print('Working directory will be: ' + idir)
print('Output directory will be: ' + odir)
print('Using alignment file: ' + aln)
print('Output JAR tree will be named: ' + tree)

print("Time to germinate!")

aln_f = Path(idir+aln)


##########################################
#                                        #
#             Main program               #
#                                        #
##########################################

##########################################
# Check if alignment file exists
##########################################

if not os.path.isfile(aln_f):
    print("Unable to find the alignment file")
    sys.exit()

##########################################
# Run IQ Tree to get that tree goodness
##########################################


p = subprocess.call("iqtree -s %s -m GTR+G -nt AUTO -bb 1000"%(aln_f), shell=True,    stdout=subprocess.PIPE,stderr=subprocess.PIPE)

tree_f = Path(idir+aln+'.treefile')

##########################################
# Check if that tree goodness exists
##########################################


if not os.path.isfile(tree_f):
    print("IQtree has failed. Sad Face.")
    sys.exit()

##########################################
# Run PyJAR for joint ancestral reconstruction
##########################################


p = subprocess.call("pyjar.py -a %s -t %s -o %s"%(aln_f,tree_f,tree), shell=True,    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
jar_f = Path(idir+tree+'.joint.tre')

if not os.path.isfile(jar_f):
    print("PyJar has failed. Sad Face.")
    sys.exit()

print()
print("Germination complete! Enjoy your new tree mate!" )
print("Its name is " + str(tree+'.joint.tre') + ". Please take care of it." )