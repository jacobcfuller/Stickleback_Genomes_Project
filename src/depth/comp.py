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


def log_all(avgDFDict):
    for x in avgDFDict:
        log(avgDFDict, x)


def log(avgDFDict, pop):
    '''Take the log difference of selected population's averaged read depth
    compared to total populations group.
    input:
        avgDF = the average of all averaged populations
        avgDFDict = a dictionary of each average population
        pop = choice for comparison
    '''
    avgDF = avgAll(avgDFDict, pop)

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
                    logX = math.log2(row[pop_column]/row['Avg'])
                    logDF.set_value(index, log_column, logX)

    # save table for downstream analysis
    logDF.to_csv(pop+".csv")
    return(logDF)


def main():
        avgDFDict, pop_covs = depth.cov(depth.avg_pops())

        log_all(avgDFDict)
        
        #logDF = log(avgDFDict, pop)

# ======================== #
#           Main           #
# ======================== #


if __name__ == '__main__':

    main()
