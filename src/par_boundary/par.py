#!/home/jcfuller/anaconda3/bin/python3.5


import math
import pandas as pd
import numpy as np


# will adjust later to take in any file - now just for testing
def makeDF(logTxt):
    #POM544_POF543 = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Japan_Sea/unmasked/JS537M_JS553F_unmasked.txt"
    #POM544_POF543 = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Pacific_Ocean/unmasked/POM544_POF543_unmasked.txt"
    #POM544_POF543 = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Paxton_lake/pax10_POM543_unmasked.txt"
    #POM544_POF543 = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Pacific_Ocean/masked/POM544_POF543_masked.txt"
    #POM544_POF543 = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Paxton_lake/pax10_JSF553_unmasked.txt"
    #POM544_POF543 = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Japan_Sea/masked/JS537M_JS553F_masked.txt"
    df = pd.read_csv(logTxt)
    bp = np.arange(len(df))

    # create true bp position, not just index count
    bp = bp * 250
    bp = bp + 2200000

    logDF = pd.DataFrame(index=bp, dtype=float)

    # create new DF with log values and accurate bp pos index
    logDF['log'] = df['log(male/female)'].values

    narrowDF = logDF.loc[2500000:2900000]
    return(narrowDF)


def findBoundary(logDF):
    for index in range(len(logDF)):
        winCount = 0
        winSum = 0
        logAvg = 4
        if ((index+100) < len(logDF)):
            for x in range(100):
                # If nan, not inf, and less than 1 (male cov shouldn't be >1)
                if(math.isnan(logDF.iloc[index+x, 0]) is False and
                   math.isinf(logDF.iloc[index+x, 0]) is False and
                   logDF.iloc[index+x, 0] < 1):
                        winCount += 1
                        winSum = winSum + logDF.iloc[index+x, 0]

            if(winCount > 0):
                logAvg = winSum / winCount
            print(logAvg)

        if logAvg <= -.5 and winCount > 75:
            print(index)
            return(logDF.iloc[index].name)


# ======================== #
#           Main           #
# ======================== #

if __name__ == '__main__':

    DF = makeDF()
    index = findBoundary(DF)
    print(index)
