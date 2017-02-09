#!/home/jcfuller/anaconda3/bin/python3.5

import pandas as pd
import depth
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
    # new = dict()
    # for x in avgDFDict:
    #     if x != pop:
    #         new[x] = avgDFDict[x]

    avgDF = (pd.concat((avgDFDict[x] for x in avgDFDict), axis=1)).mean(axis=1)
    return(avgDF)


def graph(avgDF, avgDFDict, pop):
    #fig, ax = plt.subplots()
    plt.figure(num=1, figsize=(15, 5))
    avgDFmean = avgDF.mean()
    avgPop = avgDFDict[pop].mean()
    print(avgDFmean)
    print(avgPop)
    if(avgPop > avgDFmean):
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
    else:
        plt.fill_between(avgDF.index,
                         avgDF,
                         alpha=1,
                         color='c',
                         linewidth=0,
                         label='avg')
        plt.fill_between(avgDF.index,
                         avgDFDict[pop],
                         alpha=1,
                         color='b',
                         linewidth=0,
                         label=pop)
    plt.ylim(0, 30)
    plt.legend(loc='best')
    plt.title(pop + " compared to other pops avg'd")
    plt.autoscale(axis='x', tight=True)
    plt.savefig(pop+".pdf",
                format='pdf',
                bbox_inches='tight')


avgDFDict = depth.makePopsAvgDF()

pop = getInput(avgDFDict)

avgDF = avgAll(avgDFDict, pop)
graph(avgDF, avgDFDict, pop)
