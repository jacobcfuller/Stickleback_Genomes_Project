#!/home/jcfuller/anaconda3/bin/python3.5

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def importDepth(folderPath, cov):
    depthDF = pd.concat((pd.read_table(folderPath+f,
                                       header=0,
                                       compression='gzip')
                         for f in os.listdir(folderPath)), axis=1)
    covArray = pd.read_table(cov, header=None)
    maxCov = covArray.max(numeric_only=True)
    # multiply coverage by ratio of (maxCov in pop/indCov) to normalize
    for col in list(depthDF):
        for i in covArray.index:
            if col == covArray.iloc[i, 0]:
                depthDF[col] = depthDF[col] * (maxCov.values/covArray.iloc[i, 1])

    return(depthDF)


# change input to lists later
def avgPops(df1, df2, cov1, cov2):
    cov1DF = pd.read_table(cov1, header=None)
    cov2DF = pd.read_table(cov2, header=None)
    max1 = cov1DF.max(numeric_only=True)
    max2 = cov2DF.max(numeric_only=True)
    # Normalize coverage
    if max1.values > max2.values:
        for col in list(df2):
            for i in cov2DF.index:
                if col == cov2DF.iloc[i, 0]:
                    df2[col] = df2[col] * (max1.values/cov2DF.iloc[i, 1])
    else:
        for col in list(df1):
            for i in cov1DF.index:
                if col == cov1DF.iloc[i, 0]:
                    df1[col] = df1[col] * (max2.values/cov1DF.iloc[i, 1])

    avgDF = pd.DataFrame()
    avgDF['G1_L'] = df1.mean(axis=1)
    avgDF['LW_M'] = df2.mean(axis=1)
    #print(avgDF)
    return(avgDF)


def graphDepth(df, out):
    df.plot(kind='area',
            figsize=(15, 5),
            linewidth=0,
            stacked=False,
            alpha=0.5)
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

    G1_L_Dir = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Y_chr/G1_L/win/"
    G1_L_cov = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Y_chr/G1_L/G1_L.cov"
    G1_L_DF = importDepth(G1_L_Dir, G1_L_cov)
    G1_R_Dir = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Y_chr/LW_M/win/"
    G1_R_cov = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/data/depth_analysis/Y_chr/LW_M/LW_cov"
    G1_R_DF = importDepth(G1_R_Dir, G1_R_cov)

    avgDF = avgPops(G1_L_DF, G1_R_DF, G1_L_cov, G1_R_cov)

    graphDepth(avgDF, "test")
