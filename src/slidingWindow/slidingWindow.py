#!/home/jcfuller/anaconda3/bin/python3.5

import pandas as pd
import numpy as np
import subprocess
import argparse


# Set up parser
ScriptDescript = '''Sliding Window function on SNP calls'''
Parser = argparse.ArgumentParser(description=ScriptDescript)
Parser.add_argument('-w', '--window', type=int, metavar='W', required=False, default=500,
                    help='Length of the sliding window')
#Parser.add_argument('-i', '--increment', type=int, metavar='I', required=False, default=250,
#                    help='Increment by which to slide window')
Parser.add_argument('file', type=str, metavar='F')

# Read args
args = vars(Parser.parse_args())

# make objects from args
window = args['window']
#incr = args['increment']
file = args['file']
del args

chrXIX = 20612724

# make list of 0s length of chrXIX. varPresent[chrXIX-1] = pos 20612724 (0 index array)
varPresent = [0 for x in list(range(0, chrXIX))]

# import list of SNP variant locations from vcf.table
vcfVarList = np.genfromtxt(file, dtype=int, skip_header=1, usecols=0)

# replace 0 in varPresent list with 1 at every bp position there exists a SNP
for i in range(len(vcfVarList)):
    varLocation = vcfVarList[i]
    varPresent[varLocation-1] = 1

numWin = int(chrXIX / window)

slidWinCount = np.arange(numWin)

for x in range(numWin):
    counter=0
    for i in range(500):
        if(varPresent[i+(500*x)] == 1):
            counter += 1
    slidWinCount[x] = counter






