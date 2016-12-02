#!/home/jcfuller/anaconda3/bin/python3.5


import argparse
import pandas
import math
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'Jacob C. Fuller'

chrXIX = 20612724

# ======================== #
#       Functions          #
# ======================== #


def locationFinder(logDF):
    '''does not work yet
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


def plotLogDF(logDF, output, inputFile):
    '''Create .png image of log(male/female) plot
    '''
    NCount = np.loadtxt("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/src/par_boundary/NCount.txt")
    posInfDF, negInfDF = getInfTable(logDF)
    xData = (logDF.index+getSkipRows(inputFile))*getInputWinIncr(inputFile)
    yData = logDF['log(male/female)']
    plt.figure(num=1, figsize=(12, 6))
    plt.title("log2 "+output, size=14)
    plt.xlabel('bpPos', size=12)
    plt.ylabel('log(maleCov/femaleCov)', size=12)
    plt.plot(xData,
             yData,
             'bo',
             alpha=0.5,
             ms=4.0,
             mec='blue',
             mew=0.0,
             label='log2(male/female)')
    plt.plot(xData,
             NCount,
             'mo',
             #alpha=0.5,
             ms=4.0,
             mec='magenta',
             mew=0.0,
             label='N region')
    posInf = posInfDF['posInf']
    plt.plot(xData,
             posInf,
             'yo',
             #alpha=0.3,
             ms=4.0,
             mec='yellow',
             mew=0.0,
             label='log2() = inf')
    negInf = negInfDF['negInf']
    plt.plot(xData,
             negInf,
             'ro',
             #alpha=0.3,
             ms=4.0,
             mec='red',
             mew=0.0,
             label='log2() = -inf')
    plt.legend(loc='best')
    plt.autoscale(tight=True)
    plt.savefig(output+".pdf", format='pdf', bbox_inches='tight')


def getSubSet(inputFile):
    '''Return the relevant subset of the table to be analyzed.
       Header set to 0.
    '''
    rowsToSkip = getSkipRows(inputFile)
    footerToSkip = getSkipFooter(inputFile)
    fileSubSet = pandas.read_table(
                                   inputFile,
                                   engine='python',
                                   skiprows=rowsToSkip,
                                   skipfooter=footerToSkip,
                                   header=None
                                              )
    return fileSubSet


def takeMaleFemaleLog(male, female):
    '''Takes male and female DataFrames and produces a new log2(male/female)
       DataFrame.
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
            if male.iloc[x, 0] == 0:
                logX = -np.inf
            if female.iloc[x, 0] == 0:
                logX = np.inf
        logDF.iloc[x, 0] = logX
    return logDF


def getInfTable(logDF):
    infIndex = np.arange(len(logDF))
    posInfDF = pandas.DataFrame(index=infIndex,
                                columns=['posInf'])
    for x in range(len(logDF)):
        if np.isinf(logDF.iloc[x, 0]) and np.sign(logDF.iloc[x, 0]) == 1:
            posInfDFValue = 0
        else:
            posInfDFValue = np.nan
        posInfDF.iloc[x, 0] = posInfDFValue

    negInfDF = pandas.DataFrame(index=infIndex,
                                columns=['negInf'])
    for x in range(len(logDF)):
        if np.isinf(logDF.iloc[x, 0]) and np.sign(logDF.iloc[x, 0]) == -1:
            negInfDFValue = 0
        else:
            negInfDFValue = np.nan
        negInfDF.iloc[x, 0] = negInfDFValue
    return posInfDF, negInfDF


def getRatio(male, female):
    '''Find male/female coverage ratio. Multiply maleSubset by returned value
    '''
    ratio = female/male
    return ratio


def getNumLines(inputFile):
    '''Counts the number of lines for input file. Subtract one for header. '''
    # Subtract 1 for header
    numLines = sum(1 for line in open(inputFile)) - 1
    return numLines


def getInputWinIncr(inputFile):
    '''Determines window size from previous sliding window in pipeline. '''
    numLines = getNumLines(inputFile)
    inputIncr = chrXIX/numLines
    return int(inputIncr)


def getSkipRows(inputFile):
    '''Figures out how many values to skip at top of text file. '''
    inputIncr = getInputWinIncr(inputFile)
    numRowsToSkip = 2200000/inputIncr
    return int(numRowsToSkip)


def getSkipFooter(inputFile):
    '''Figures out how many values to leave out at bottom of text file. '''
    inputIncr = getInputWinIncr(inputFile)
    numRowsToExlcude = int(17612724/inputIncr)
    return numRowsToExlcude


def getTrueBPLocation(inputFile, logDF):
    numRowsSkipped = getSkipRows(inputFile)
    inputIncr = getInputWinIncr(inputFile)
    location = locationFinder(logDF)
    location += numRowsSkipped
    location = location * inputIncr
    return(location)


def getLogTable(mFile, fFile, mReads, fReads):
    ratio = getRatio(mReads, fReads)
    maleSubSet = getSubSet(mFile)
    femaleSubSet = getSubSet(fFile)
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

    plotLogDF(logMaleFemale, output, maleFile)

    logMaleFemale.to_csv(output+".txt")

    #print(output+" "+str(trueLocation)+" "+str(locationIndex))
