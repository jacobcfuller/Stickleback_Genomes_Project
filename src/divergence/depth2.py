#!/home/jcfuller/anaconda3/bin/python3.5

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

depthDirPath = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Y_chr/"


def importDepth():
    popDFs = dict()
    for d in os.listdir(depthDirPath):
        if os.path.isdir(depthDirPath+d):
            df = pd.concat((pd.read_table(depthDirPath+d+'/win/'+f,
                                          header=0,
                                          compression='gzip')
                            for f in os.listdir(depthDirPath+d+'/win/')), axis=1)
            popDFs[d] = df
    return(popDFs)


def avgPops(DFdict):
    # table population with their individual aligned read counts
    tablePath = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/doc/reads.csv"
    # import into dataframe, only use individual name column with associated read
    reads = pd.read_csv(tablePath, usecols=['Ind', 'Aligned Reads'])

    # Go through each population stored in DFdict, and normalize read counts
    popReads = dict()
    absMax = 0
    for x in DFdict:
        print(x)
        # x = pop group
        maxRead = 0
        for ind in list(DFdict[x]):
            # ind = name of an individual in population/col in DF
            # ind in depth_table = eg "BS44_Y", but read table just "BS44".
            # get rid of Y to index correctly
            name = ind[:len(ind)-2]
            indRead = reads.loc[reads['Ind'] == name]['Aligned Reads'].values.item(0)
            popReads[ind] = int(indRead)

            print(ind, popReads[ind])

            if(popReads[ind] > maxRead):
                maxRead = popReads[ind]

        print(maxRead)

        if(maxRead > absMax):
            absMax = maxRead
        for ind in list(DFdict[x]):
            print(ind, (maxRead/popReads[ind]))

            df = DFdict[x]
            df[ind] = df[ind] * (maxRead/popReads[ind])


def graphDepth(dfAVGdict, out):
    for df in dfAVGdict:
        print(df)
        dfAVGdict[df].plot(kind='area',
                           figsize=(15, 5),
                           linewidth=0,
                           stacked=False,
                           alpha=0.5)
    plt.legend(labels=dfAVGdict)
    plt.title("Read Depth")
    plt.autoscale(axis='x', tight=True)
    plt.autoscale(axis='x', tight=True)
    plt.savefig(out+".pdf",
                format='pdf',
                bbox_inches='tight')


# ======================== #
#           Main           #
# ======================== #


if __name__ == '__main__':

    #parser = argparse.ArgumentParser(description='depth')
    #parser.add_argument('-c', '--cov', type=str, metavar='C', required=True)
    #parser.add_argument('-o', '--out', type=str, metavar='O', required=True)
    #parser.add_argument('folder', metavar='F', type=str, help='path to file')
    #args = vars(parser.parse_args())
#
    #out = args['out']
    #cov = args['cov']
    #df = importDepth(args['folder'], cov)
    dfdict = importDepth()
    avg = avgPops(dfdict)
    #graphDepth(avg, "test")
