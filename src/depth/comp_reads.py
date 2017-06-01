#!/home/jcfuller/anaconda3/bin/python3.6

import pandas as pd
import os


def import_reads():
    '''Import bp read depth files into DataFrame from pwd
    Folder must contain only depth files

    returns
    -------
    total_df - DataFrame
    '''
    total_df = pd.concat((pd.read_csv(f, header=0)
                          for f in os.listdir(os.getcwd())), axis=1)

    return total_df
