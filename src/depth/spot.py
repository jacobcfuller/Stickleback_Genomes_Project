#!/home/jcfuller/anaconda3/bin/python3.5

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


csv_path = "filter/"


def import_log():
    '''Go into subdirectories to fetch all sliding window depth files

    output: Dictionary of population DataFrames
    '''
    pos_csv = dict()
    neg_csv = dict()
    for f in os.listdir(csv_path):
        if "pos" in f:
            df = pd.read_csv(csv_path+f)
            name = str(f)[:str(f).find(".filter")]
            pos_csv[name] = df
        elif "neg" in f:
            df = pd.read_csv(csv_path+f)
            name = str(f)[:str(f).find(".filter")]
            neg_csv[name] = df

    return(pos_csv, neg_csv)


# pull out regions with log and
def get_reg():
    pos_csv, neg_csv = import_log()
    for x in pos_csv:
        with open("reg/"+x+".reg", 'w') as output:
            output.write("bp_pos"+'\t'+"log"+'\n')
            # row = (0)index, (1)avg, (2)pop, (3)log
            for index, row in pos_csv[x].iterrows():
                if(row[3] > 0):
                    output.write(str(row[0])+'\t'+str(row[3])+'\n')
    for x in neg_csv:
        with open("reg/"+x+".reg", 'w') as output:
            output.write("bp_pos"+'\t'+"log"+'\n')
            # row = (0)index, (1)avg, (2)pop, (3)log
            for index, row in neg_csv[x].iterrows():
                if(row[3] < 0):
                    output.write(str(row[0])+'\t'+str(row[3])+'\n')


# ======================== #
#           Main           #
# ======================== #


if __name__ == '__main__':

    get_reg()
