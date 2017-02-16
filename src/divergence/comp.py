#!/home/jcfuller/anaconda3/bin/python3.5

import math
import depth
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


N_txt = ("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/src/"
         "divergence/Y_N_count.txt")

N_df = pd.read_csv(N_txt)


def getInput(avgDFDict):
    for x in avgDFDict:
        print(x)
    inputWrong = True
    while(inputWrong):
        pop = input("Choose a population to compare to other pops:")
        if pop in avgDFDict:
            inputWrong = False
        else:
            print('Try Again')
            inputWrong = True
    return(pop)


def avgAll(avgDFDict, pop):
    avgDF = (pd.concat((avgDFDict[x] for x in avgDFDict), axis=1)).mean(axis=1)
    return(avgDF)


def getInfTable(logDF):
    infIndex = np.arange(len(logDF))
    posInfDF = pd.DataFrame(index=infIndex,
                            columns=['posInf'])
    for x in range(len(logDF)):
        if np.isinf(logDF.iloc[x, 0]) and np.sign(logDF.iloc[x, 0]) == 1:
            posInfDFValue = 0
        else:
            posInfDFValue = np.nan
        posInfDF.iloc[x, 0] = posInfDFValue

    negInfDF = pd.DataFrame(index=infIndex,
                            columns=['negInf'])
    for x in range(len(logDF)):
        if np.isinf(logDF.iloc[x, 0]) and np.sign(logDF.iloc[x, 0]) == -1:
            negInfDFValue = 0
        else:
            negInfDFValue = np.nan
        negInfDF.iloc[x, 0] = negInfDFValue
    return posInfDF, negInfDF


def log(avgDF, avgDFDict, pop):
    # all populations averaged together
    totalMeanDF = avgDF
    # Average of population chosen for comparison
    avgPop = avgDFDict[pop]
    logDF = pd.DataFrame(index=np.arange(len(totalMeanDF)),
                         columns=["log("+pop+"/avg)"])

    for x in range(len(totalMeanDF)):
        logX = math.log2(totalMeanDF[x]/avgPop[x])
        if(N_df.iloc[x, 0] == 0):
            logDF.iloc[x, 0] = np.nan
        else:
            # might need to swap these
            if avgPop[x] == 0:
                logX = -np.inf
            if totalMeanDF[x] == 0:
                logX = np.inf
            logDF.iloc[x, 0] = logX

    return(logDF)


def graph(logDF):
    pos_inf, neg_inf = getInfTable(logDF)

    plt.figure(num=1, figsize=(15, 5))
    plt.plot(logDF,
             'bo',
             alpha=0.5,
             ms=4.0,
             mec='blue',
             mew=0.0,
             label='log2('+pop+'/avg)')
    plt.plot(pos_inf,
             'yo',
             ms=4.0,
             mec='yellow',
             mew=0.0,
             label='pos_inf')
    plt.plot(neg_inf,
             'go',
             ms=4.0,
             mec='green',
             mew=0.0,
             label='neg_inf')
    plt.plot(N_df,
             'ro',
             ms=4.0,
             mec='red',
             mew=0.0,
             label='N')
    # plt.ylim(-4, 20)
    plt.xlabel('bpPos', size=12)
    plt.ylabel("log2("+pop+"/avg)", size=12)
    plt.legend(loc='best')
    plt.title(pop + " compared to other pops avg'd")
    plt.autoscale(axis='x', tight=True)
    plt.savefig(pop+".pdf",
                format='pdf',
                bbox_inches='tight')


# ======================== #
#           Main           #
# ======================== #


if __name__ == '__main__':

    avgDFDict = depth.makePopsAvgDF()

    pop = getInput(avgDFDict)

    avgDF = avgAll(avgDFDict, pop)

    log_df = log(avgDF, avgDFDict, pop)
    graph(log_df)
