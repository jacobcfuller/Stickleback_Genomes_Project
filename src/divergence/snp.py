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
                                  index_col=0,
                                  dtype=float)
                    for f in os.listdir(snp_folder)), axis=1)
    return(df)


def import_reads_avg():
    '''Import csv containing read depth average for each populatin.
    Multiply index by 1000 to represent true bp position.
    '''
    reads_df = pd.read_table("pops_avg_reads.csv", sep=',', index_col=0)
    reads_df.index = reads_df.index * 1000
    return(reads_df)


def snp_filter():
    '''if reads < 5, set snps to np.nan
    return new filtered df
    '''
    output_path = ("/home/jcfuller/Documents/White_lab/"
                   "Stickleback_Genomes_Project/data/")
    reads_df = import_reads_avg()
    snps_df = import_snps()
    for pop in list(snps_df):
        data = {'reads': reads_df[pop], 'snps': snps_df[pop]}
        df = pd.DataFrame(data, index=snps_df.index, dtype=float)
        for index, row in df.iterrows():
            if(row['reads'] < 5):
                snps_df.set_value(index, pop, np.nan)
    return(snps_df)


def avg_all(filtered_snps):
    '''get avg snp count at every bp pos, from all pops.
    exclude np.nan
    return series with this info.
    '''
    return(filtered_snps.mean(axis=1, numeric_only=True))


def set_avg_all_denom(filtered_snps):
    '''divide each position by avg snp count per kb
    '''
    total_snps, total_pos = 0, 0
    avg_all_filtered = avg_all(filtered_snps)
    for index, value in avg_all_filtered.iteritems():
        if np.isfinite(value):
            total_snps += value
            total_pos += 1
    avg = float(total_snps / total_pos)
    avg_all_filtered = avg_all_filtered/avg
    return(avg_all_filtered)


def get_pop_snp_avgs(filtered_snps):
    '''get avg # of snps per 1000 bp window across Y

    Return dict of averages.
    '''
    total_snps, total_pos = 0, 0
    snps_avg = dict()

    for pop in list(filtered_snps):
        for index, value in filtered_snps[pop].iteritems():
            if np.isfinite(value):
                total_snps += value
                total_pos += 1
        snps_avg[pop] = (total_snps / total_pos)
        total_pos, total_snps = 0, 0
    return(snps_avg)


def set_denom(filtered_snps):
    '''For each population, divide the snp count by avg snp count per kb
    '''
    snps_avg = get_pop_snp_avgs(filtered_snps)

    for pop in list(filtered_snps):
        filtered_snps[pop] = filtered_snps[pop]/snps_avg[pop]
    return(filtered_snps)


def log(filtered_snps):
    '''get log2(pop/avg)
    set to np.nan if pop has read depth of 0 at index
    return dataframe
    '''
    snps_df = set_denom(filtered_snps)
    avg = set_avg_all_denom(filtered_snps)
    log_df = pd.DataFrame(index=snps_df.index, columns=list(snps_df))
    for pop in list(snps_df):
        for index, value in snps_df[pop].iteritems():
            # can't do log(0/x) or log(x/0)
            if(value == 0 and avg.loc[index] > 0):
                log_df[pop].set_value(index, -np.inf)
            elif(value > 0 and avg.loc[index] == 0):
                log_df[pop].set_value(index, np.inf)
            elif(value == 0 and avg.loc[index] == 0):
                log_df[pop].set_value(index, 0)
            else:
                log = math.log2(value/avg.loc[index])
                log_df[pop].set_value(index, log)

    return(log_df)


def filter_nan(log_df):
    '''Makes table of only areas where read depth is good.
    i.e., drop rows where any column is NAN. Only keep data where all can be compared
    '''
    log_df = log_df.dropna()
    return(log_df)

filter_nan(log(snp_filter())).to_csv("dropna.csv", ",")
