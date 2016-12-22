#!/home/jcfuller/anaconda3/bin/python3.5

'''Find par boundary with 2 sliding windows that run over log2(male/female)
read depth files
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


# gets first last and middle avgs. Only really need middle.
# kept others for testing
def getFirstMidLastAvg(logDF):
    firstDF = logDF.loc[2200000:2300000]
    lastDF = logDF.loc[2899500:2999500]
    first = firstDF['log'].mean()
    last = lastDF['log'].mean()
    middle = (first+last)/2
    return(first, middle, last)


#def infSpot(logDF, winSize, win2Sep):


def parFinder(logTxtFile):
    logDF = makeDF(logTxtFile)
    first, middle, last = getFirstMidLastAvg(logDF)
    win2Sep = 20000
    winSize = 10000
    indexComp = winSize+15000
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
            print("index:", (index+indexComp),
                  "1:", win1Avg['log'],
                  "2:", win2Avg['log'],
                  "avg:", avg)
            #if(math.isclose(avg, middle, abs_tol=0.01) and
            #   (first+.05) > win1Avg['log'] and
            #   (-1) < win2Avg['log'] < middle):
            #        print(first, middle, last)
            #        return(index+indexComp)

            # Not sure how the abs_tol or rel_tol works but I think it could be useful
            if(math.isclose(avg, middle, abs_tol=0.01) and
               math.isclose(win1Avg['log'], first, abs_tol=0.1) and
               math.isclose(win2Avg['log'], last, abs_tol=0.1)):
                    print(first, middle, last)
                    return(index+indexComp)
# ======================== #
#           Main           #
# ======================== #

if __name__ == '__main__':
    # just for testing now. should return 2612750.
    parFinder("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Pacific_Ocean/unmasked/POM544_POF543_unmasked.txt")
