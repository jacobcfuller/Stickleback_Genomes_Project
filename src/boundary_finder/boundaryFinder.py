#!/home/jcfuller/anaconda3/bin/python3.5

import argparse
import pandas
import math
import numpy as np

chrXIX = 20612724

# ======================== #
#       Functions          #
# ======================== #


def logSlidingWindow(logDF):
    '''Get sliding average of log values for file subset.'''
    slidingMeans = logDF.rolling(100).mean
    return slidingMeans


def getSubSet(file, rowsToSkip, footerToSkip):
    '''Return the relevant subset of the table to be analyzed.
       Header set to 0.
    '''
    fileSubSet = pandas.read_table(file, engine='python', skiprows=rowsToSkip,
                                   skipfooter=footerToSkip, header=None)
    return fileSubSet


def takeMaleFemaleLog(male, female):
    '''Takes male and female DataFrames and produces a new log2(male/female)
       DataFrame, setting log2(0/0) to nan.
    '''
    logDF = pandas.DataFrame()
    for x in range(len(male)):
        malex = male.iloc[x, 0]
        femalex = female.iloc[x, 0]
        if malex != 0 and femalex != 0:
            logX = math.log2(malex/femalex)
        else:
            logX = np.nan
        logDF[x, 0] = logX
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
    rowToSkip = getSkipRows(250)
    footerToSkip = getSkipFooter(250)

    maleSubset = getSubSet("Win_1000_incr_250_POM544_XIX_depth.txt", rowToSkip,
                           footerToSkip)
    femaleSubset = getSubSet("Win_1000_incr_250_POF_543_XIX.txt", rowToSkip,
                             footerToSkip)

    logDF = takeMaleFemaleLog(maleSubset, femaleSubset)

    slidingMeans = logSlidingWindow(logDF)
    print(slidingMeans)
