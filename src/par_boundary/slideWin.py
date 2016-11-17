#!/home/jcfuller/anaconda3/bin/python3.5

'''GetChunks gets average for each chunk pulled out.
slidingWin does rolling average of the above averages.

GetChunks "chunksize" sets the number of points, while SlidingWin adjusts
how smooth each average will be
THIS IS GENIUS

stolen from Lucas A. Nell
'''
import pandas as pd
import subprocess as sp

# ======================== #
#       Functions          #
# ======================== #


def GetChunks(File):
    '''Function to read raw depths and create a pd.DataFrame of chunk means.

    Outputs pd.DataFrame for next step.
    '''

    RawDepthTab = pd.read_table(
                                File,
                                compression='gzip',
                                delim_whitespace=True,
                                chunksize=5000)

    ChunkAvgs = (chunk.mean() for chunk in RawDepthTab)

    Length = int(sp.check_output('gunzip -c %s | wc -l' % File, shell=True).strip()) - 1

    return pd.DataFrame(ChunkAvgs), Length


def CleanEnd(RollingChunks, ChunkAvgs, Length):
    '''Adjusts last rolling-chunk average for uneven last-chunk length.

    Args:
        RollingChunks (pd.DataFrame): Table of rolling chunk averages.
        ChunkAvgs (pd.DataFrame): Table of chunk-mean averages.
        Length (int): Length of sequence.
        ind (int): Index of column you're fixing.

    Returns:
        (float): New rolling-chunk average.
    '''
    Partial = Length % Incr  # Size of last chunk (!=Incr)
    Avg0 = RollingChunks.iloc[-1, 0]
    End = ChunkAvgs.iloc[-1, 0]
    # Sum of all chunk avgs other than end one
    NonEnd = (Avg0 * chuWin) - End
    # New sum of chunk averages, where End is underweighted
    Total = (End * (Partial / Incr)) + NonEnd
    # New chuWin, where End is underweighted
    EndN = (chuWin - 1) + (Partial / Incr)
    return Total / EndN


def SlidingWin(ChunkAvgDF, Length):
    '''Create table of read-depth averages across a sliding window.

    Args:
        ChunkAvgDF (pd.DataFrame): Table of chunk averages.
        Length (int): Total length of sequence.

    Returns:
        Nothing. Writes output to file.
    '''
    # Calculates a rolling mean of length 'chuWin', then shifts it so it starts
    # with numbers, then it removes the NaN at the end
    RollingChunks = ChunkAvgDF.rolling(window=2).mean().dropna() \
                              .reset_index(drop=True)
    RollingChunks.iloc[-1, 0] = CleanEnd(RollingChunks, ChunkAvgDF, Length, 0)

    return RollingChunks

DF, length = GetChunks("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/\
depth_analysis/Paxton_lake/raw_coverage/PB_male10_q_XIX.txt.gz")
print(DF)
