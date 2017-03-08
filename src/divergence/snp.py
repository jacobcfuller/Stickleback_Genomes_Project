#!/home/jcfuller/anaconda3/bin/python3.5

import os
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
