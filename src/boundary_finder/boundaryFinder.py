#!/home/jcfuller/anaconda3/bin/python3.5

import argparse
import pandas
import math
import numpy as np

chrXIX = 20612724

# ======================== #
#       Functions          #
# ======================== #


def locationFinder(logDF):
    x = 0
    logAvg = 0
    while(x < len(logDF) and logAvg >= 0):
        logSum = 0
        avgCounter = 0
        logAvg = 0

        if (math.isnan(logDF.iloc[x, 0]) is False):
            # 100 value window
            if((x+100) < len(logDF)):
                for i in range(100):
                    if(math.isnan(logDF.iloc[(x+i), 0]) is False):
                        avgCounter += 1
                        logSum = logSum + logDF.iloc[(x+i), 0]
                logAvg = logSum/avgCounter
                x += 100
            else:
                break
        else:
            x += 1
    x = x - 100

    y = x - 10
    logAvg = 0
    while(y < (x+50) and logAvg >= 0):
        logSum = 0
        avgCounter = 0
        logAvg = 0
        if (math.isnan(logDF.iloc[y, 0]) is False):
            # 10 value window
            if((y+10) < len(logDF)):
                for i in range(10):
                    if(math.isnan(logDF.iloc[(y+i), 0]) is False):
                        avgCounter += 1
                        logSum = logSum + logDF.iloc[(y+i), 0]
                logAvg = logSum/avgCounter
                y += 10
            else:
                break
        else:
            y += 1
    y = y - 10
    return(y)


def getSubSet(file, rowsToSkip, footerToSkip):
    '''Return the relevant subset of the table to be analyzed.
       Header set to 0.
    '''
    fileSubSet = pandas.read_table(
                                   file,
                                   engine='python',
                                   skiprows=rowsToSkip,
                                   skipfooter=footerToSkip,
                                   header=None
                                              )
    return fileSubSet


def takeMaleFemaleLog(male, female):
    '''Takes male and female DataFrames and produces a new log2(male/female)
       DataFrame, setting log2(0/0) to nan.
       Compensates for coverage difference.
    '''
    maleSum = male.sum()
    femaleSum = female.sum()
    if(maleSum[0] > femaleSum[0]):
        female = female*(maleSum[0]/femaleSum[0])
    else:
        male = male*(femaleSum[0]/maleSum[0])

    logDF = pandas.DataFrame(
                             index=np.arange(len(male)),
                             columns=['log(male/female)']
                                                         )
    for x in range(len(male)):
        if male.iloc[x, 0] != 0 and female.iloc[x, 0] != 0:
            logX = math.log2(male.iloc[x, 0]/female.iloc[x, 0])
        else:
            logX = np.nan
        logDF.iloc[x, 0] = logX
    return logDF


def getNumLines(file):
    '''Counts the number of lines for input file. Subtract one for header. '''
    # Subtract 1 for header
    numLines = sum(1 for line in open(file)) - 1
    return numLines


def getInputWinIncr(numLines):
    '''Determines window size from previous sliding window in pipeline. '''
    inputIncr = chrXIX/numLines
    return int(inputIncr)


def getSkipRows(inputIncr):
    '''Figures out how many values to skip at top of text file. '''
    numRowsToSkip = 1500000/inputIncr
    return int(numRowsToSkip)


def getSkipFooter(inputIncr):
    '''Figures out how many values to leave out at bottom of text file. '''
    numRowsToExlcude = int(16112724/inputIncr)
    return numRowsToExlcude

# ======================== #
#           Main           #
# ======================== #

if __name__ == '__main__':
    rowsToSkip = getSkipRows(250)
    footerToSkip = getSkipFooter(250)

    male = getSubSet(
                     "Win_1000_incr_250_POM544_XIX_depth.txt",
                     rowsToSkip,
                     footerToSkip
                                 )
    female = getSubSet(
                       "Win_1000_incr_250_POF_543_XIX.txt",
                       rowsToSkip,
                       footerToSkip
                                   )
    logDF = takeMaleFemaleLog(male, female)
    #for x in range(len(logDF)):
    #    print(logDF.iloc[x, 0])
    locationFinder(logDF)
