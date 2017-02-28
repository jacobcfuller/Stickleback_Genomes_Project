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


# pull out regions and print to file
def get_reg():
    pos_csv, neg_csv = import_log()
    for x in pos_csv:
        with open("reg/"+x+".reg", 'w') as output:
            output.write("bp_pos" + "\t" +
                         "Avg. depth" + "\t" +
                         x + " depth" + "\t" +
                         "log" + "\n")
            # row = (0)index, (1)avg, (2)pop, (3)log
            for index, row in pos_csv[x].iterrows():
                if(row[3] > 0):
                    output.write(str(row[0]) + '\t' +
                                 str(row[1]) + '\t' +
                                 str(row[2]) + '\t' +
                                 str(row[3])+'\n')
    for x in neg_csv:
        with open("reg/"+x+".reg", 'w') as output:
            output.write("bp_pos" + "\t" +
                         "Avg. depth" + "\t" +
                         x + " depth" + "\t" +
                         "log" + "\n")
            # row = (0)index, (1)avg, (2)pop, (3)log
            for index, row in neg_csv[x].iterrows():
                if(row[3] < 0):
                    output.write(str(row[0]) + '\t' +
                                 str(row[1]) + '\t' +
                                 str(row[2]) + '\t' +
                                 str(row[3])+'\n')


# combine into master table
def get_table():
    regs = []
    pop_regs = dict()
    # get all regions
    for f in os.listdir("reg"):
        df = pd.read_table("reg/"+f, usecols=[0, 3])
        pop_regs[f] = df
        array = np.genfromtxt("reg/"+f, skip_header=1, usecols=0)
        for x in array:
            if x not in regs:
                regs.append(x)
    regs.sort()

    # get column names for master DataFrame
    cols = []
    pos_csv, neg_csv = import_log()
    for x in list(pos_csv):
        cols.append(x[:x.find(".pos")])
    DF_master = pd.DataFrame(columns=cols, index=regs)
    DF_master.index.names = ['Var. regions']

    # pop_reg columns = "bp_pos", "log"
    for df in pop_regs:
        name = df[:df.find(".")]
        for index, row in pop_regs[df].iterrows():
            DF_master.set_value(row['bp_pos'], name, row['log'])

    return(DF_master)


def main():
    # get_reg()
    DF_master = get_table()
    DF_master.to_csv("test", sep='\t')

# ======================== #
#           Main           #
# ======================== #


if __name__ == '__main__':
    main()
