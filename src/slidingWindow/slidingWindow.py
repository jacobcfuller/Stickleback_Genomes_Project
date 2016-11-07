#!/home/jcfuller/anaconda3/bin/python3.5

import numpy as np
import argparse


# Set up parser
ScriptDescript = '''Sliding Window function on SNP calls'''
Parser = argparse.ArgumentParser(description=ScriptDescript)
Parser.add_argument('-w', '--window', type=int, metavar='W', required=False,
                    default=500, help='Length of the sliding window')
Parser.add_argument('file', type=str, metavar='F')

# Read args
args = vars(Parser.parse_args())

# Make objects from args
window = args['window']
file = args['file']
del args

chrXIX = 20612724

# Make list of 0s length of chrXIX. varPresent[chrXIX-1] = pos 20612724
# (0 index array)
varPresent = [0 for x in list(range(0, chrXIX))]

# Import list of SNP variant locations from vcf.table
vcfVarList = np.genfromtxt(file, dtype=int, skip_header=1, usecols=0)

# Replace 0 in varPresent list with 1 at every bp position there exists a SNP
for i in range(len(vcfVarList)):
    varLocation = vcfVarList[i]
    varPresent[varLocation-1] = 1

# Get number of windows
numWin = int(chrXIX / window)

# Creat array to place SNP counts for each window
slidWinCount = np.arange(numWin)

# For loop multiplies window count to get actual bp pos for varPresent array
# Counts SNPs for each 500bp increment. last few hundred bp cut off.
# Not interested in knowing SNP count at end, because PAR boundary isn't near
# there
for x in range(numWin):
    counter = 0
    for i in range(window):
        if(varPresent[i+(window*x)] == 1):
            counter += 1
    slidWinCount[x] = counter


np.savetxt(file+"_slidWin"+str(window), slidWinCount, fmt='%i')
