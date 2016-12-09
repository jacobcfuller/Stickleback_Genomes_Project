#!/home/jcfuller/anaconda3/bin/python3.5
'''Algorithm designed to locate the PAR boundary based on Log2(male/female)
coverage data. It's not particularly fast...
'''

import math
import pandas as pd
import numpy as np


# will adjust later to take in any file - now just for testing
def makeDF(logTxtFile):
    df = pd.read_csv(logTxtFile)
    bp = np.arange(len(df))

    # create true bp position, not just index count
    bp = bp * 250
    bp = bp + 2200000

    logDF = pd.DataFrame(index=bp, dtype=float)

    # create new DF with log values and accurate bp pos index
    logDF['log'] = df['log(male/female)'].values

    narrowDF = logDF.loc[2500000:2900000]
    return(narrowDF)


def findBoundary(logTxtFile):
    logDF = makeDF(logTxtFile)
    for index in range(len(logDF)):
        winCount = 0
        winSum = 0
        logAvg = 4
        if ((index+100) < len(logDF)):
            for x in range(100):
                # If nan, not inf, and less than 1 (male cov shouldn't be >1)
                if(math.isnan(logDF.iloc[index+x, 0]) is False and
                   math.isinf(logDF.iloc[index+x, 0]) is False and
                   logDF.iloc[index+x, 0] < 1 and
                   logDF.iloc[index+x, 0] > -2):
                        winCount += 1
                        winSum = winSum + logDF.iloc[index+x, 0]

            if(winCount > 0):
                logAvg = winSum / winCount

        if logAvg <= -.75 and winCount > 75:
            return(logDF.iloc[index].name)
