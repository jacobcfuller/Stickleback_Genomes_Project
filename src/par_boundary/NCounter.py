#!/home/jcfuller/anaconda3/bin/python3.5

'''Program to count the # of Ns in a fasta file. in a window of 250 bp, if more
than half are N, this goes as "1" otherwise 0. prints list of 1/0
'''

chrXIX = open('chrXIX.fa')

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
        if NCount > 125:
            NCountList.append(1)
        else:
            NCountList.append(0)
        NCount = 0
        print(NCountList[index])
        index += 1

chrXIX.close()
