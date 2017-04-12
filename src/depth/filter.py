#!/home/jcfuller/anaconda3/bin/python3.5

import argparse
import depth
import os
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


def filter_all():
    for f in os.listdir("."):
        if ".csv" in f:
            logDF = pd.read_csv(f, index_col=0)
            filterLog(logDF)


def filterLog(logDF):
    '''Get rid of values that mean nothing
    '''
    cov = depth.pop_covs(depth.avg_pops())

    # asign as variables for easier reading
    avg_col = list(logDF)[0]
    pop_col = list(logDF)[1]
    log_col = list(logDF)[2]

    # make new DataFrames for both pos and neg
    pos_log = pd.DataFrame(columns=[avg_col, pop_col, log_col])
    neg_log = pd.DataFrame(columns=[avg_col, pop_col, log_col])
    # if both avg_col and pop_col are <5, or log too low, set to Nan
    print(pop_col, cov[pop_col])
    min_cov = (5/cov[pop_col])
    for index, row in logDF.iterrows():
        if ((row[avg_col] < min_cov and row[pop_col] < min_cov) or
           (row[log_col] < 0.5)):
            pos_log.set_value(index, avg_col, np.nan)
            pos_log.set_value(index, pop_col, np.nan)
            pos_log.set_value(index, log_col, np.nan)
        else:
            pos_log.set_value(index, avg_col, row[avg_col])
            pos_log.set_value(index, pop_col, row[pop_col])
            pos_log.set_value(index, log_col, row[log_col])

    pos_log.to_csv("filter/"+pop_col+".pos.filter.csv")
    # if both avg_col and pop_col are <5, or log too high, set to Nan
    for index, row in logDF.iterrows():
        if ((row[avg_col] < min_cov and row[pop_col] < min_cov) or
           (row[log_col] > -0.5)):
            neg_log.set_value(index, avg_col, np.nan)
            neg_log.set_value(index, pop_col, np.nan)
            neg_log.set_value(index, log_col, np.nan)
        else:
            neg_log.set_value(index, avg_col, row[avg_col])
            neg_log.set_value(index, pop_col, row[pop_col])
            neg_log.set_value(index, log_col, row[log_col])

    neg_log.to_csv("filter/"+pop_col+".neg.filter.csv")

    return(pos_log, neg_log)


def graph(logDF):
    x = range(len(logDF))
    y = logDF[list(logDF)[2]]

    plt.figure(num=1, figsize=(15, 5))
    plt.plot(x,
             y)
    plt.savefig(list(logDF)[1]+".pdf", format='pdf', bbox_inches='tight')


filter_all()
