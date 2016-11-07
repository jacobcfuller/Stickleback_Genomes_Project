#!/home/jcfuller/anaconda3/bin/python3.5

import argparse
import pandas

chrXIX = 20612724

#========================#
#       Functions        #
#========================#

def getSubsetAvgs(file,rowsToSkip,footerToSkip):
    fileChunksSubset = pandas.read_table(file,skiprows=rowsToSkip,skipfooter=footerToSkip, chunksize=100)
    chunkAvgs = chunk.mean() for chunk in fileChunksSubset
    return pandas.DataFrame(chunkAvgs)

def takeMaleFemaleLog(male,female):
    

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
