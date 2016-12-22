#!/home/jcfuller/anaconda3/bin/python3.5

'''Find par boundary with 2 sliding windows that run over log2(male/female)
read depthfiles
'''

import math
import pandas as pd
import numpy as np


# make logDF with log.txt and add index with correct bp pos
def makeDF(logTxtFile):
    df = pd.read_csv(logTxtFile)
    bp = np.arange(len(df))

    # create true bp position, not just index count
    bp = bp * 250
    bp = bp + 2200000

    logDF = pd.DataFrame(index=bp, dtype=float)

    # create new DF with log values and accurate bp pos index
    logDF['log'] = df['log(male/female)'].values

    # remove inf and -inf
    for x in range(len(logDF)):
        if np.isinf(logDF.iloc[x, 0]):
            logDF.iloc[x, 0] = np.nan

    return(logDF)


# gets first last and middle avgs
def getFirstMidLastAvg(logDF):
    firstDF = logDF.loc[2200000:2300000]
    lastDF = logDF.loc[2899500:2999500]
    first = firstDF['log'].mean()
    last = lastDF['log'].mean()
    middle = (first+last)/2
    return(first, middle, last)


def parFinder(logTxtFile):
    logDF = makeDF(logTxtFile)
    first, middle, last = getFirstMidLastAvg(logDF)
    win2Sep = 20000
    winSize = 10000
    win1Avg = 123
    win2Avg = 345
    # index is true bp loc in this loop, and there are 2000 indices
    for index in logDF.index:
        # keep window in dataframe - 2 50000 bp window, separated by 10000
        if (index+win2Sep+winSize) < 2900000:
            win1Avg = logDF.loc[index:(index+winSize)].mean()
            win2Avg = (logDF.loc[(index+win2Sep):(index+win2Sep+winSize)]
                       .mean())
            avg = (win1Avg['log']+win2Avg['log'])/2
            if(math.isclose(avg, middle, abs_tol=0.01)):
                print("middle:", middle)
                print("avg:", avg)
                print("index:", index+winSize+15000)


# ======================== #
#           Main           #
# ======================== #

if __name__ == '__main__':
    parFinder("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Pacific_Ocean/unmasked/POM544_POF543_unmasked.txt")
