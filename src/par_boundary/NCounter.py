#!/home/jcfuller/anaconda3/bin/python3.5

import numpy as np

'''Program to count the # of Ns in a fasta file. in a window of 250 bp, if more
than half are N, this goes as "1" otherwise 0. prints list of 1/0
'''

chrXIX = open("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/chrXIX.fa")

# header line
line = chrXIX.readline

NCountList = []
index = 0
lineCount = 0
NCount = 0
while line:
    line = chrXIX.readline()
    lineCount += 1
    for base in line:
        if base == 'N':
            NCount += 1
    if lineCount is 5:
        lineCount = 0
        if NCount >= 125:
            NCountList.append(0)
        else:
            NCountList.append(float('nan'))
        NCount = 0
        index += 1
chrXIX.close()

subset = NCountList[8800:14399]

nplist = np.asarray(subset)

np.savetxt("NCount.txt", nplist)
