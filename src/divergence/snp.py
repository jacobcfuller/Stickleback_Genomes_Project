#!/home/jcfuller/anaconda3/bin/python3.5

import os
import math
import numpy as np
import pandas as pd

snp_folder = ("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/"
              "data/snps/unique_snps")


def import_snps():
    '''import all .snps files from snp_folder into one dataframe.
    return dataframe
    '''
    df = pd.concat((pd.read_table(snp_folder+'/'+f,
                                  header=0,
                                  index_col=0)
                    for f in os.listdir(snp_folder)), axis=1)
    return(df)


def avg_all(df):
    '''get avg snp count at every bp pos, from all pops.
    return series with this info.
    '''
    return(df.mean(axis=1))


def log(df):
    '''get log2(pop/avg)
    set to np.nan if pop has read depth of 0 at index
    return dataframe
    '''
    avg = avg_all(df)
    log_df = pd.DataFrame(index=df.index, columns=list(df))
    reads_df = pd.read_table("pops_avg_reads.csv", sep=',', index_col=0)
    reads_df.index = reads_df.index * 1000
    for pop in list(df):
        for index, value in df[pop].iteritems():
            # read depth = 0
            if(index < 12180000 and reads_df.loc[index][pop] == 0):
                log_df[pop].set_value(index, np.nan)
            # can't do log(0/x) or log(x/0)
            elif(value == 0 and avg.loc[index] > 0):
                log_df[pop].set_value(index, -np.inf)
            elif(value > 0 and avg.loc[index] == 0):
                log_df[pop].set_value(index, np.inf)
            elif(value == 0 and avg.loc[index] == 0):
                log_df[pop].set_value(index, 0)
            else:
                log = math.log2(value/avg.loc[index])
                log_df[pop].set_value(index, log)

    return(log_df)


log_df = log(import_snps())
log_df.to_csv('snps.csv')
