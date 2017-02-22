#!/home/jcfuller/anaconda3/bin/python3.5

import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def getLogDF():
    # Set up parser
    # can't handle bad input yet
    ScriptDescript = '''Filter out useless/misleading data'''
    parser = argparse.ArgumentParser(description=ScriptDescript)
    parser.add_argument('csv_file', metavar='F', type=str)
    args = vars(parser.parse_args())
    csv_file = args['csv_file']

    logDF = pd.read_csv(csv_file, index_col=0)
    return(logDF)


def filterLog(logDF):
    '''Get rid of values that mean nothing
    '''
    # asign as variables for easier reading
    avg_col = list(logDF)[0]
    pop_col = list(logDF)[1]
    log_col = list(logDF)[2]

    # if both avg_col and pop_col are <5, set to Nan
    for index, row in logDF.iterrows():
        if row[avg_col] < 5 and row[pop_col] < 5:
            logDF.set_value(index, avg_col, np.nan)
            logDF.set_value(index, pop_col, np.nan)
            logDF.set_value(index, log_col, np.nan)
    logDF.to_csv(pop_col+".filter.csv")
    return(logDF)


def graph(logDF):
    x = range(len(logDF))
    y = logDF[list(logDF)[2]]

    plt.figure(num=1, figsize=(20, 5))
    plt.plot(x,
             y)
    plt.savefig(list(logDF)[1]+".pdf", format='pdf', bbox_inches='tight')


graph(filterLog(getLogDF()))
