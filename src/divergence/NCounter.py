#!/home/jcfuller/anaconda3/bin/python3.5

import numpy as np

chrY = open("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/doc/Y_Chr_JoinedAssembly.fa")

# header line
line = chrY.readline()

NCountList = []
win = 0
NCount = 0
while line:
    line = chrY.readline()
    for base in line:
        win += 1
        if base is 'N':
            NCount += 1
        if win == 1000:
            win = 0
            if NCount >= 500:
                NCountList.append(0)
            else:
                NCountList.append(float('nan'))
            NCount = 0
chrY.close()

nplist = np.asarray(NCountList[0:12147])

np.savetxt("NCount.txt", nplist)
