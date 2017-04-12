#!/home/jcfuller/anaconda3/bin/python3.6
'''Functions to analyze output of window_percent.py'''

import os
import glob
import pandas as pd


def import_csv():
    '''import each individual into a dataframe
    change ">5 %" column to name of individual

    returns df
    '''
    folder_path = ("/home/jcfuller/Documents/White_lab/"
                   "Stickleback_Genomes_Project/data/depth_analysis/Y_chr/"
                   "percentage_windows/male/")
    # get all abs paths to files
    files = glob.glob(os.path.join(folder_path, "*.csv"))
    # get individual names from path string
    names = [f.split("_win.csv")[0].split("/male/")[1] for f in files]
    # import into df
    total_df = pd.concat((pd.read_csv(f, header=0, usecols=[1])
                         for f in files), axis=1)
    # make index = bp pos
    total_df.index = total_df.index * 1000
    # change columns to real names from above
    total_df.columns = names
    return(total_df)


def find_win(percentage):
    '''Find windows where all individuals are above .80
    returns (filter_df, no_na_df)
    '''
    df = import_csv()
    filter_df = df[df > percentage]
    no_na_df = filter_df.dropna(how='any')

    return(filter_df, no_na_df)


filter_df, no_na_df = find_win(.8)

filter_df.to_csv("filtered.csv")
no_na_df.to_csv("no_na.csv")
