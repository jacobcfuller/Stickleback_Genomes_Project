#!/home/jcfuller/anaconda3/bin/python3.5

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

# folder structured like this:
# population/win/indivualSlidingWindowDepth.file
depthDirPath = ("/home/jcfuller/Documents/White_lab/"
                "Stickleback_Genomes_Project/"
                "data/depth_analysis/Y_chr/")


def importDepth():
    '''Go into subdirectories to fetch all sliding window depth files

    output: Dictionary of population DataFrames
    '''
    popDFs = dict()
    for d in os.listdir(depthDirPath):
        if os.path.isdir(depthDirPath+d):
            df = pd.concat((pd.read_table(depthDirPath+d+'/win/'+f,
                                          header=0,
                                          compression='gzip')
                            for f in os.listdir(depthDirPath+d+'/win/')), axis=1)
            popDFs[d] = df
    return(popDFs)


def normPops(DFdict):
    '''Imports table of individual aligned read counts into DataFrame. Finds
    the highest read count, then multiplies all others by (highest/individual).

    input:DataFrame from importDepth().
    output: normalized version of DFdict
    '''
    # table population with their individual aligned read counts
    tablePath = ("/home/jcfuller/Documents/White_lab/"
                 "Stickleback_Genomes_Project/doc/reads.csv")
    # import into dataframe, only use individual name column with associated read
    reads = pd.read_csv(tablePath, usecols=['Ind', 'Aligned Reads'])

    # Go through each population stored in DFdict, and get highest read count
    popReads = dict()
    absMax = 0
    for x in DFdict:
        # x = pop group
        maxRead = 0
        for ind in list(DFdict[x]):
            # ind = name of an individual in population/col in DF
            # ind in depth_table = eg "BS44_Y", but read table just "BS44".
            # get rid of Y to index correctly
            name = ind[:len(ind)-2]
            indRead = reads.loc[reads['Ind'] == name]['Aligned Reads'].values.item(0)
            popReads[ind] = int(indRead)
            if(popReads[ind] > maxRead):
                maxRead = popReads[ind]
        if(maxRead > absMax):
            absMax = maxRead

    # normalize read count
    for x in DFdict:
        df = DFdict[x]
        for name in list(DFdict[x]):
            df[name] = df[name] * (absMax/popReads[name])
        DFdict[x] = df

    return(DFdict)


# need to figure out naming for graph
def avgPops(DFdict):
    popAvgDict = dict()
    for x in DFdict:
        df = DFdict[x]
        popAvgDict[x] = df.mean(axis=1)

    return(popAvgDict)


def makePopsAvgDF():
    ''' Put all functions together and return a dictionary of dataframes,
    each of which are the averaged read depth of the given populations
    '''
    dfdict = importDepth()
    normDict = normPops(dfdict)
    popAvgDict = avgPops(normDict)
    return(popAvgDict)


def graphDepth(dfAVGdict, out):
    for df in dfAVGdict:
        dfAVGdict[df].plot(kind='area',
                           legend=True,
                           figsize=(15, 5),
                           linewidth=0,
                           stacked=False,
                           alpha=0.5)
    plt.title("Read Depth")
    plt.autoscale(axis='x', tight=True)
    plt.savefig(out+".pdf",
                format='pdf',
                bbox_inches='tight')


# ======================== #
#           Main           #
# ======================== #


if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='depth')
    # parser.add_argument('-c', '--cov', type=str, metavar='C', required=True)
    # parser.add_argument('-o', '--out', type=str, metavar='O', required=True)
    # parser.add_argument('folder', metavar='F', type=str, help='path to file')
    # args = vars(parser.parse_args())

    dfdict = importDepth()
    dfdict = normPops(dfdict)
    popAvgDict = avgPops(dfdict)
    graphDepth(popAvgDict, "test")
