#!/home/jcfuller/anaconda3/bin/python3.6
'''Program to perform sliding window Pi(nucleotide diversity) stats.
Must account for missing data.
'''
import os
import numpy as np
import pandas as pd


def import_pi():
    '''make dictionary of series with names from file (w/o '.pi')
    '''
    folder = ("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/"
              "data/Pi_sites/")
    pi_dict = dict()
    for f in os.listdir(folder):
        df = pd.read_table(folder + f, usecols=(1, 2))
        name = f[:4]
        pi_dict[name] = df
    return(pi_dict)


def import_reads():
    '''import pops avg reads into dataframe. return dataframe
    '''
    reads = 'pops_avg_reads.csv'
    reads_df = pd.read_csv(reads)
    reads_df.index = reads_df.index * 1000
    return(reads_df)


def slide():
    reads_df = import_reads()
    pi_dict = import_pi()

    for pop in pi_dict:
        col = pop + " PI"
        pi_df = pd.DataFrame(data={col: np.nan}, index=reads_df.index)
        loc = 0
        avg = 0
        avg_count = 0
        for index, row in pi_dict[pop].iterrows():
            if(row['POS'] >= loc and row['POS'] < (loc + 1000)):
                avg += row['PI']
                avg_count += 1
            else:
                if(avg > 0):
                    pi = (avg / (1000))
                    pi_df.set_value(loc, col, pi)
                else:
                    pi_df.set_value(loc, col, 0)
                avg = row['PI']
                avg_count = 1
                while(row['POS'] > (loc + 1000)):
                    loc += 1000

        print(pi_df)
        break


slide()
