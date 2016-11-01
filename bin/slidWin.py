#!/usr/bin/env python3

"""Sliding Window function on raw read depth files genomecov.

Note: No normalization based on chr19 reads is done here. That is saved for R scripts.
-wd needs to be directory with files
"""


import pandas as pd
import subprocess as sp
import argparse
from timeit import default_timer as timer
from multiprocessing import Pool

__author__ = 'Lucas A. Nell'






# ========================================================================================
# ========================================================================================
# ========================================================================================
# ========================================================================================

#               FUNCTIONS

# ========================================================================================
# ========================================================================================
# ========================================================================================
# ========================================================================================

# -----------------------------
#       Raw depths --> Chunks
# -----------------------------

def GetChunks(File):

    """Function to read raw depths and create a pd.DataFrame of chunk means.

    Outputs pd.DataFrame for next step."""

    RawDepthTab = pd.read_table(File, compression='gzip',
                                delim_whitespace=True, chunksize=Incr)

    ColNames = list(RawDepthTab.get_chunk(1))
    ChunkAvgs = [[chunk[name].mean() for name in ColNames] for chunk in RawDepthTab]

    Length = int(sp.check_output('gunzip -c %s | wc -l' % File, shell=True).strip()) - 1

    return pd.DataFrame(ChunkAvgs, columns = ColNames), Length




# -----------------------------
#       Chunks  -->  Windows
# -----------------------------


def CleanEnd(RollingChunks, ChunkAvgs, Length, ind):

    """Adjusts last rolling-chunk average for uneven last-chunk length.

    Args:
        RollingChunks (pd.DataFrame): Table of rolling chunk averages.
        ChunkAvgs (pd.DataFrame): Table of chunk-mean averages.
        Length (int): Length of sequence.
        ind (int): Index of column you're fixing.

    Returns:
        (float): New rolling-chunk average.
    """
    Partial = Length % Incr  # Size of last chunk (!=Incr)
    Avg0 = RollingChunks.iloc[-1, ind]
    End = ChunkAvgs.iloc[-1, ind]
    # Sum of all chunk avgs other than end one
    NonEnd = (Avg0 * chuWin) - End
    # New sum of chunk averages, where End is underweighted
    Total = ( End * (Partial / Incr) ) + NonEnd
    # New chuWin, where End is underweighted
    EndN = (chuWin - 1) + (Partial / Incr)
    return Total / EndN



def SlidingWin(ChunkAvgDF, Length):

    """Create table of read-depth averages across a sliding window.

    Args:
        ChunkAvgDF (pd.DataFrame): Table of chunk averages.
        Length (int): Total length of sequence.

    Returns:
        Nothing. Writes output to file.
    """
    ColNames = list(ChunkAvgDF)
    # Calculates a rolling mean of length 'chuWin', then shifts it so it starts with
    # numbers, then it removes the NaN at the end
    RollingChunks = ChunkAvgDF.rolling(window = chuWin).mean().dropna().reset_index(drop = True)
    for i in range(len(ColNames)):
        RollingChunks.iloc[-1, i] = CleanEnd(RollingChunks, ChunkAvgDF, Length, i)
    return RollingChunks



# -----------------------------
#       Putting steps together
#       -wd needs to be directory with files
# -----------------------------

def ForTheWin(File):
    """Give it a file name, it'll run AllTheChunks and SlidingWin, saving output."""
    t0 = timer()
    ChunkAvgDF, Length = GetChunks(File)
    RollingChunks = SlidingWin(ChunkAvgDF, Length)
    #following OutFile line only works if given file argument is the name of file
    #not the name of the path of the file
    OutFile = 'Win_'+str(Window)+'_incr_'+str(Incr)+'_' + File
    RollingChunks.to_csv(OutFile, index = False, sep = '\t', compression = 'gzip',
                         float_format = '%-0.5f')
    print('~' * 40)
    print('Total time to create %s was %.2f seconds' % (OutFile, timer() - t0))
    print('~' * 40)









# ========================================================================================
# ========================================================================================
# ========================================================================================
# ========================================================================================

#               READING INPUT ARGUMENTS, CREATING OBJECTS

# ========================================================================================
# ========================================================================================
# ========================================================================================
# ========================================================================================


# -----------------------------
# Setting up parser
# -----------------------------
ScriptDescript = '''Sliding Window function on raw read depth files. -wd needs to be directory with files'''

Parser = argparse.ArgumentParser(description = ScriptDescript)
Parser.add_argument('-w', '--window', type = int, metavar = 'W',
                    required = False, default = 1000,
                    help = 'Length of the sliding window')
Parser.add_argument('-i', '--increment', type = int, metavar = 'I',
                    required = False, default = 500,
                    help = 'Increment by which to slide window')
Parser.add_argument('files', type = str, metavar = 'F', nargs = '+',
                    help = 'Raw depth (ending in ".txt.gz") file(s)')
Parser.add_argument('-t', '--threads', type = int, metavar = 'T',
                    required = False, default = 1,
                    help = 'How many threads can this use? The default is 1 ' + \
                           '(not useful to have more threads than files).')



# -----------------------------
# Now reading the arguments
# -----------------------------
args = vars(Parser.parse_args())


# -----------------------------
#   Making objects
# -----------------------------

Threads = args['threads']
Window = args['window']
Incr = args['increment']
Files = args['files']
del args  # No longer needed


# Number of chunks per Window
chuWin = int(Window / Incr)


assert (Window % Incr) == 0, 'Window size must be a multiple of the increment size.'

assert Threads >= 1, "You specified < 1 thread. This makes 0 sense."



# ========================================================================================
# ========================================================================================
# ========================================================================================
# ========================================================================================

#               RUNNING PROGRAM ON INPUT DATA

# ========================================================================================
# ========================================================================================
# ========================================================================================
# ========================================================================================



# Now running functions on all filenames given, parallel or serial
if __name__ == '__main__':
    if Threads > 1:
        with Pool(processes = Threads) as pool:
            pool.map(ForTheWin, Files)
    else:
        for f in Files:
            ForTheWin(f)
