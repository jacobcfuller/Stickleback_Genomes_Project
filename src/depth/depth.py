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


def import_depth():
    '''Go into subdirectories to fetch all sliding window depth files

    output: Dictionary of population DataFrames.
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


def norm_pops(DFdict):
    '''Imports table of individual aligned read counts into DataFrame. Finds
    the highest read count, then multiplies all others by (highest/individual).

    input:DataFrame from import_depth().
    output: normalized version of DFdict
    '''
    # table population with their individual aligned read counts
    tablePath = ("/home/jcfuller/Documents/White_lab/"
                 "Stickleback_Genomes_Project/doc/project_misc/reads.csv")
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
def avg_pops():
    '''DFdict contains a dictionary of dataframes. Each dataframe contains
    a population, where each column in the dataframe is an individual.

    Returns a new dictionary of dataframes (or Series, rather), where each
    DataFrame is the average of all individuals in a population.
    '''
    DF_dict = import_depth()
    norm_dict = norm_pops(DF_dict)

    popAvgDict = dict()
    for x in norm_dict:
        df = norm_dict[x]
        popAvgDict[x] = df.mean(axis=1)

    return(popAvgDict)


def pop_covs(popAvgDict):
    pop_covs = dict()
    for name in list(popAvgDict):
        pop_covs[name] = popAvgDict[name].mean()
    return(pop_covs)


def cov(popAvgDict):
    '''Get the average coverage on the Y chromosome for each population.

    Change avg pops dataframe. make values = (orig. value/avg cov)
    '''
    pop_covs = dict()
    for name in list(popAvgDict):
        pop_covs[name] = popAvgDict[name].mean()

    for df_name, df_pop in popAvgDict.items():
        for index, value in df_pop.iteritems():
            df_pop.set_value(index, (value/pop_covs[df_name]))

    return(popAvgDict, pop_covs)


def main():
    cov(avg_pops())
