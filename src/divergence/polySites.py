#!/home/jcfuller/anaconda3/bin/python3.5

# Must remove 82M19 unorder scaffold before using this

import pandas as pd


def makeDF(snpTable):
    snpDF = pd.read_table(snpTable, low_memory=False)

    return snpDF


# This shit's recursive, y'all
def fillInZeros(maleDF, index, winCount):
    mDF = maleDF
    if(mDF.iloc[index+1]['POS'] >= (1000*(winCount))):
        print((1000*(winCount)), '\t', '0')
        winCount += 1
        return fillInZeros(mDF, index, winCount)
    else:
        return winCount


def slideWindow(mDF, fDF, incr):
    snpCount = 0
    winCount = 1

    # remember DF is 0-index
    for index in mDF.index:
        #print(index)
        # If SNP call doesn't exist in female, count
        if((mDF.iloc[index]['POS'] in fDF['POS'].values) is False):
            snpCount += 1
        # if end of 1000bp window, record stat
        if(mDF.iloc[index+1]['POS'] >= (1000*winCount)):
            print((1000*winCount), '\t', snpCount)
            # reset counter
            snpCount = 0
            # check if there are actually snps in the next window
            winCount += 1
            winCount = fillInZeros(mDF, index, winCount)


# ======================== #
#           Main           #
# ======================== #


if __name__ == '__main__':
    # tests
    Fdf = makeDF('/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/snps/LW_F.table')
    Mdf = makeDF('/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/snps/LW_M.table')
    print("pos", '\t', 'snp #')
    slideWindow(Mdf, Fdf, 1)
