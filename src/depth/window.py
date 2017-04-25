#!/usr/bin/env python

# change ^ if not running on UGA Sapelo


import argparse
import pandas as pd


def import_reads(depth):
    df = pd.read_table(depth, header=0)
    return(df)


def slide(depth_value, reads_df):
    '''for 1kb window, find percentage of nonzero and percentage
    at specified depth
    slow cus O(n) :(
    '''
    spec_depth = []
    bp_count = 0
    spec_count = 0
    not_count = 0
    win = 0
    for index, value in reads_df.iterrows():
        bp_count += 1
        if(value[0] >= depth_value):
            spec_count += 1
        else:
            not_count += 1
        if(bp_count == 1000):
            win += 1
            bp_count = 0
            if(spec_count > 0):
                spec_depth.append(spec_count / 1000)
            else:
                spec_depth.append(0)
            spec_count = 0
            not_count = 0
    data = {('>' + str(depth_value) + ' %'): spec_depth}
    df = pd.DataFrame(data)
    return(df)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('depth_file', metavar='F', type=str)
    args = vars(parser.parse_args())
    depth_file = args['depth_file']
    reads_df = import_reads(depth_file)
    df = slide(5, reads_df)
    df.to_csv(depth_file.split("_depth")[0] + "_win.csv")


run()
