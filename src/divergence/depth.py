#!/home/jcfuller/anaconda3/bin/python3.5

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def importDepth(folderPath, cov):
    depthDF = pd.concat((pd.read_table(f,
                                       header=0,
                                       compression='gzip')
                         for f in os.listdir(folderPath)), axis=1)
    covArray = pd.read_table(cov, header=None)
    maxCov = covArray.max(numeric_only=True)
    depthDF.to_csv("../G1_L_noncomp.txt", sep='\t')
    # multiply coverage by ratio of (maxCov in pop/indCov) to normalize
    for col in list(depthDF):
        for i in covArray.index:
            if col == covArray.iloc[i, 0]:
                depthDF[col] = depthDF[col] * (maxCov.values/covArray.iloc[i, 1])
    depthDF.to_csv("../G1_L_comp.txt", sep='\t')
    return(depthDF)


def graphDepth(df):
    plt.figure(num=1, figsize=(15, 5))
    plt.stackplot(df.index, df.T, linewidth=0)
    #plt.ylim([0, 20])
    plt.title("Read Depth")
    plt.autoscale(axis='x', tight=True)
    plt.autoscale(axis='x', tight=True)
    plt.savefig("../depth.pdf",
                format='pdf',
                bbox_inches='tight')


# ======================== #
#           Main           #
# ======================== #


if __name__ == '__main__':

    #df = importDepth('/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Y_chr/LW_M/slideWin10000')
    parser = argparse.ArgumentParser(description='depth')
    parser.add_argument('-c', '--cov', type=str, metavar='C', required=True)
    parser.add_argument('folder', metavar='F', type=str, help='path to file')
    args = vars(parser.parse_args())

    cov = args['cov']
    df = importDepth(args['folder'], cov)

    graphDepth(df)
