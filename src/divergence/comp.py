#!/home/jcfuller/anaconda3/bin/python3.5

import pandas as pd
import numpy as np
import depth
import math
import matplotlib.pyplot as plt


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


# Include or exlude pop to compare??

def avgAll(avgDFDict, pop):
    avgDF = (pd.concat((avgDFDict[x] for x in avgDFDict), axis=1)).mean(axis=1)
    return(avgDF)


def log(avgDF, avgDFDict, pop):
    # all populations averaged together
    totalMeanDF = avgDF
    print(totalMeanDF)
    # Average of population chosen for comparison
    avgPop = avgDFDict[pop]
    print(avgPop)
    logDF = pd.DataFrame(index=np.arange(len(totalMeanDF)),
                         columns=["log("+pop+"/avg)"])

    for x in range(len(totalMeanDF)):
        logX = math.log2(totalMeanDF[x]/avgPop[x])
        logDF.iloc[x, 0] = logX

    plt.figure(num=1, figsize=(15, 5))

    plt.plot(logDF,
             'bo',
             alpha=0.5,
             ms=4.0,
             mec='blue',
             mew=0.0)
    #plt.ylim(-4, 20)
    plt.xlabel('bpPos', size=12)
    plt.ylabel("log2("+pop+"/avg)", size=12)
    plt.title(pop + " compared to other pops avg'd")
    plt.autoscale(axis='x', tight=True)
    plt.savefig(pop+".pdf",
                format='pdf',
                bbox_inches='tight')


def graphBoth(avgDF, avgDFDict, pop):
    #fig, ax = plt.subplots()
    plt.figure(num=1, figsize=(15, 5))
    avgDFmean = avgDF.mean()
    avgPop = avgDFDict[pop].mean()
    print(avgDFmean)
    print(avgPop)

    plt.fill_between(avgDF.index,
                     avgDFDict[pop],
                     alpha=1,
                     color='b',
                     linewidth=0,
                     label=pop)
    plt.fill_between(avgDF.index,
                     avgDF,
                     alpha=1,
                     color='c',
                     linewidth=0,
                     label='avg')

    plt.ylim(0, 30)
    plt.legend(loc='best')
    plt.title(pop + " compared to other pops avg'd")
    plt.autoscale(axis='x', tight=True)
    plt.savefig(pop+"both.pdf",
                format='pdf',
                bbox_inches='tight')


avgDFDict = depth.makePopsAvgDF()

pop = getInput(avgDFDict)

avgDF = avgAll(avgDFDict, pop)

log(avgDF, avgDFDict, pop)
#graphBoth(avgDF, avgDFDict, pop)
