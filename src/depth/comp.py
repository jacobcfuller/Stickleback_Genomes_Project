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
    '''Take the log difference of selected population's averaged read depth
    compared to total populations group.
    input:
        avgDF = the average of all averaged populations
        avgDFDict = a dictionary of each average population
        pop = choice for comparison
    '''
    log_column = ("log("+pop+"/Avg)")
    pop_column = str(pop)
    logDF = pd.DataFrame(index=np.arange(len(avgDF)),
                         columns=["Avg", pop_column, log_column])
    logDF['Avg'] = avgDF
    logDF[pop_column] = avgDFDict[pop]

    # I think this is best way to go through dataframe
    for index, row in logDF.iterrows():
        # 0 = N present on reference. Set to nan.
        if(N_df.iloc[index, 0] == 0):
            logDF.set_value(index, log_column, np.nan)
        else:
            # if both are 0, set to 0
            if row['Avg'] == 0 and row[pop_column] == 0:
                logDF.set_value(index, log_column, 0)
            else:
                # if pop is 0, set to -inf
                if row[pop_column] == 0.0:
                    logDF.set_value(index, log_column, -np.inf)
                # if avg is 0, set to +inf
                elif row['Avg'] == 0.0:
                    logDF.set_value(index, log_column, np.inf)
                # if everything clean, get log
                else:
                    logX = math.log2(row['Avg']/row[pop_column])
                    logDF.set_value(index, log_column, logX)

    # save table for downstream analysis
    logDF.to_csv(pop+".csv")
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
             label='inf')
    plt.plot(neg_inf,
             'yo',
             ms=4.0,
             mec='yellow',
             mew=0.0)
    plt.plot(N_df,
             'ro',
             ms=4.0,
             mec='red',
             mew=0.0,
             label='N')
    plt.ylim(-4, 4)
    plt.xlabel('bpPos', size=12)
    plt.ylabel("log2("+pop+"/avg)", size=12)
    plt.legend(bbox_to_anchor=(0, 0, 1, 1),
               loc=0,
               numpoints=1,
               prop={'size': 8})
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
    #graph(log_df)
