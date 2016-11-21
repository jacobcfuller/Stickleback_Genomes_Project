#!/home/jcfuller/anaconda3/bin/python3.5

'''getChunks gets average for each chunk pulled out.
slidingWin does rolling average of the above averages.

getChunks "chunksize" sets the number of points, while slidingWin adjusts
how smooth each average will be
THIS IS GENIUS

stolen from Lucas A. Nell
'''
import argparse
import subprocess as sp
import pandas as pd


# ======================== #
#       Functions          #
# ======================== #


def getChunks(File):
    '''Function to read raw depths and create a pd.DataFrame of chunk means.

    Outputs pd.DataFrame for next step.
    '''

    rawDepthTab = pd.read_table(File,
                                compression='gzip',
                                delim_whitespace=True,
                                chunksize=incr)

    chunkAvgs = (chunk.mean() for chunk in rawDepthTab)

    tableLength = int(sp.check_output('gunzip -c %s | wc -l' % File,
                                      shell=True)
                        .strip()) - 1

    return pd.DataFrame(chunkAvgs), tableLength


def cleanEnd(rollingChunks, chunkAvgs, tableLength):
    '''Adjusts last rolling-chunk average for uneven last-chunk tableLength.

    Args:
        rollingChunks (pd.DataFrame): Table of rolling chunk averages.
        chunkAvgs (pd.DataFrame): Table of chunk-mean averages.
        tableLength (int): tableLength of sequence.
        ind (int): Index of column you're fixing.

    Returns:
        (float): New rolling-chunk average.
    '''
    partial = tableLength % incr  # Size of last chunk (!=incr)
    avg0 = rollingChunks.iloc[-1, 0]
    end = chunkAvgs.iloc[-1, 0]
    # Sum of all chunk avgs other than end one
    nonEnd = (avg0 * chuWin) - end
    # New sum of chunk averages, where end is underweighted
    total = (end * (partial / incr)) + nonEnd
    # New chuWin, where end is underweighted
    endN = (chuWin - 1) + (partial / incr)
    return total / endN


def slidingWin(chunkAvgDF, tableLength):
    '''Create table of read-depth averages across a sliding window.

    Args:
        chunkAvgDF (pd.DataFrame): Table of chunk averages.
        tableLength (int): Total tableLength of sequence.

    Returns:
        Nothing. Writes output to file.
    '''
    # Calculates a rolling mean of tableLength 'chuWin', then shifts it so it starts
    # with numbers, then it removes the NaN at the end
    rollingChunks = (chunkAvgDF.rolling(window=chuWin)
                               .mean()
                               .dropna()
                               .reset_index(drop=True))

    rollingChunks.iloc[-1, 0] = cleanEnd(rollingChunks,
                                         chunkAvgDF,
                                         tableLength)
    return rollingChunks


def getSlidwin(depthFile):
    """Give it a file name, it'll run slidingWin, saving output."""
    chunkAvgDF, tableLength = getChunks(depthFile)
    rollingChunks = slidingWin(chunkAvgDF, tableLength)
    # following outFile line only works if given file argument is the name of file
    # not the name of the path of the file
    outFile = 'Win_'+str(window)+'_incr_'+str(incr)+'_' + depthFile
    rollingChunks.to_csv(outFile,
                         index=False,
                         sep='\t',
                         compression='gzip',
                         float_format='%-0.5f')


# ======================== #
#           Main           #
# ======================== #

if __name__ == '__main__':

    ScriptDescript = '''Sliding Window function on raw read depth files.
     -wd needs to be directory with files
     '''

    Parser = argparse.ArgumentParser(description=ScriptDescript)
    Parser.add_argument('-w',
                        '--window',
                        type=int,
                        metavar='W',
                        required=False,
                        default=1000,
                        help='Length of the sliding window')
    Parser.add_argument('-i',
                        '--increment',
                        type=int,
                        metavar='I',
                        required=False,
                        default=500,
                        help='Increment by which to slide window')
    Parser.add_argument('file',
                        type=str,
                        metavar='F',
                        help='Raw depth (ending in ".txt.gz") file')
    args = vars(Parser.parse_args())
    window = args['window']
    incr = args['increment']
    depthFile = args['file']
    chuWin = int(window/incr)
    del args  # No longer needed

    getSlidwin(depthFile)
