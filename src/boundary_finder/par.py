#!/home/jcfuller/anaconda3/bin/python3.5

'''Program to find PAR boundaries.
Returns two outputs:
    1) file of log(male/female) subset
    2) PAR location

How to deal with noise??
'''

import argparse
import pandas
import math
import numpy as np
import matplotlib.pyplot as plt

chrXIX = 20612724

# ======================== #
#       Functions          #
# ======================== #


def locationFinder(logDF):
    '''locationFinder takes the log(male/female) dataframe and runs two sliding
       windows over it. The sliding window is tracking averages, assuming the
       averages in the PAR is greater than or equal to 0. A negative
       average is indicative of female coverage being higher than male, i.e.,
       area on the chromosome that does not recombine with the X. I have thus
       defined the PAR boundary as the location where logAvg transitions from
       positive to negative.

       The first sliding window is low resolution, a window of size 100 to find
       the general area of the PAR.

       The second sliding window backs up 10 indices behind the first
       determined location, and proceeds to run a sliding window of size 10 for
       a higher resolution location.

       Returns index of logAvg dataframe corresponding to avg sign change.
    '''
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
                if(avgCounter > 70):
                    logAvg = logSum/avgCounter
                x += 100
            else:
                break
        else:
            x += 1
    x = (x - 100)

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


def plotLogDF(logDF, output, inputIncr):
    '''Create .png image of log(male/female) plot
    '''
    incr = inputIncr
    xData = (logDF.index+getSkipRows(incr))*incr
    yData = logDF['log(male/female)']
    plt.figure(num=1, figsize=(12, 6))
    plt.title('log(male/female)', size=14)
    plt.xlabel('bpPos', size=12)
    plt.ylabel('log(male/female)', size=12)
    plt.scatter(xData, yData, marker=".")
    plt.autoscale(tight=True)
    plt.savefig(output+".png", format='png', bbox_inches='tight')


def getSubSet(file):
    '''Return the relevant subset of the table to be analyzed.
       Header set to 0.
    '''
    rowsToSkip = getSkipRows(file)
    footerToSkip = getSkipFooter(file)
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
    index = np.arange(len(male))
    logDF = pandas.DataFrame(
                             index=index,
                             columns=['log(male/female)']
                                                         )
    for x in range(len(male)):
        if male.iloc[x, 0] != 0 and female.iloc[x, 0] != 0:
            logX = math.log2(male.iloc[x, 0]/female.iloc[x, 0])
        else:
            logX = np.nan
        logDF.iloc[x, 0] = logX
    return logDF


def getRatio(male, female):
    '''Find male/female coverage ratio. Multiply maleSubset by returned value
    '''
    if(male > female):
        ratio = female/male
    else:
        ratio = male/female
    return ratio


def getNumLines(file):
    '''Counts the number of lines for input file. Subtract one for header. '''
    # Subtract 1 for header
    numLines = sum(1 for line in open(file)) - 1
    return numLines


def getInputWinIncr(file):
    '''Determines window size from previous sliding window in pipeline. '''
    numLines = getNumLines(file)
    inputIncr = chrXIX/numLines
    return int(inputIncr)


def getSkipRows(file):
    '''Figures out how many values to skip at top of text file. '''
    inputIncr = getInputWinIncr(file)
    numRowsToSkip = 2200000/inputIncr
    return int(numRowsToSkip)


def getSkipFooter(file):
    '''Figures out how many values to leave out at bottom of text file. '''
    inputIncr = getInputWinIncr(file)
    numRowsToExlcude = int(17012724/inputIncr)
    return numRowsToExlcude


def getTrueBPLocation(file, logDF):
    numRowsSkipped = getSkipRows(file)
    inputIncr = getInputWinIncr(file)
    location = locationFinder(logDF)
    location += numRowsSkipped
    location = location * inputIncr
    return(location)


def getLogTable(mFile, fFile, mReads, fReads):
    numLines = getNumLines(mFile)
    ratio = getRatio(mReads, fReads)
    inputWinIncr = getInputWinIncr(numLines)
    rowsToSkip = getSkipRows(inputWinIncr)
    footerToSkip = getSkipFooter(inputWinIncr)
    maleSubSet = getSubSet(maleFile, rowsToSkip, footerToSkip)
    femaleSubSet = getSubSet(femaleFile, rowsToSkip, footerToSkip)
    maleSubSet = maleSubSet*ratio
    logMaleFemale = takeMaleFemaleLog(maleSubSet, femaleSubSet)

    return logMaleFemale

# ======================== #
#           Main           #
# ======================== #

if __name__ == '__main__':
    # Set up parser
    ScriptDescript = '''Find PAR boundary BP location'''
    Parser = argparse.ArgumentParser(description=ScriptDescript)
    Parser.add_argument('-m', '--maleFile', type=str, metavar='M', required=True)
    Parser.add_argument('-f', '--femaleFile', type=str, metavar='F', required=True)
    Parser.add_argument('-o', '--outfile', type=str, metavar='O', required=True)
    Parser.add_argument('-mr', '--malereads', type=int, metavar='MR', required=True)
    Parser.add_argument('-fr', '--femalereads', type=int, metavar='FR', required=True)
    args = vars(Parser.parse_args())

    # Set args to variables
    maleFile = args['maleFile']
    femaleFile = args['femaleFile']
    maleReads = args['malereads']
    femaleReads = args['femalereads']
    output = args['outfile']
    del args

    # Check that male & female files are the same size
    maleNumLines = getNumLines(maleFile)
    femaleNumLines = getNumLines(femaleFile)
    assert maleNumLines == femaleNumLines, "male and female files must be same size"

    logMaleFemale = getLogTable(maleFile, femaleFile, maleReads, femaleReads)

    plotLogDF(logMaleFemale, output, getInputWinIncr(maleFile))

    #logMaleFemale.to_csv(output)

    #print(output+" "+str(trueLocation)+" "+str(locationIndex))