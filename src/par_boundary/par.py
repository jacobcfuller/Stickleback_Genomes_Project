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
        win1Count = 0
        win2Count = 0
        win1Sum = 0
        win2Sum = 0
        logAvg1 = 12312
        logAvg2 = 12312
        if ((index+200) < len(logDF)):
            for x in range(100):
                # If nan, not inf, and less than 1 (male cov shouldn't be >1)
                if(math.isnan(logDF.iloc[index+x, 0]) is False and
                   math.isinf(logDF.iloc[index+x, 0]) is False and
                   logDF.iloc[index+x, 0] < 1 and
                   logDF.iloc[index+x, 0] > -2):
                        win1Count += 1
                        win1Sum = win1Sum + logDF.iloc[index+x, 0]
            for y in range(100):
                    if(math.isnan(logDF.iloc[index+y+100, 0]) is False and
                       math.isinf(logDF.iloc[index+y+100, 0]) is False and
                       logDF.iloc[index+y+100, 0] < 1 and
                       logDF.iloc[index+y+100, 0] > -2):
                            win2Count += 1
                            win2Sum = win2Sum + logDF.iloc[index+y+100, 0]
            if(win1Count > 0 and win2Count > 0):
                logAvg1 = win1Sum / win1Count
                logAvg2 = win2Sum / win2Count
