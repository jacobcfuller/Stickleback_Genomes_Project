#!/home/jcfuller/anaconda3/bin/python3.5

import argparse
import pandas
import math
import numpy as np

chrXIX = 20612724

# ======================== #
#       Functions          #
# ======================== #

# def getLogAvgs(logDataFrame):


def getSubSet(file, rowsToSkip, footerToSkip):
    fileSubSet = pandas.read_table(file, engine='python', skiprows=rowsToSkip,
                                   skipfooter=footerToSkip, header=None)
    return fileSubSet


def takeMaleFemaleLog(male, female):
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
    # Subtract 1 for header
    numLines = sum(1 for line in open(file)) - 1
    return numLines


def getInputWinIncr(numLines):
    inputIncr = chrXIX/numLines
    return int(inputIncr)


def getSkipRows(inputIncr):
    numRowsToSkip = 1500000/inputIncr
    return int(numRowsToSkip)


def getSkipFooter(inputIncr):
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
