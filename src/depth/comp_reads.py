#!/home/jcfuller/anaconda3/bin/python3.6

import pandas as pd
import os


def import_reads():
    """Import bp read depth files into DataFrame from pwd
    Folder must contain only depth files

    returns
    -------
    total_df - DataFrame
    """
    total_df = pd.concat((pd.read_csv(f, header=0)
                          for f in os.listdir(os.getcwd())), axis=1)

    return total_df


def compare(df, min_depth):
    """

    input
    -----
    df - DataFrame from import_reads()
    min_depth - int value representing minimum allowable read depth for
                analysis

    returns
    -------
    comp_df - Dataframe including only loci where bp is > min_depth in all inds
    percent - how much of Y chromosome is actually able to be looked at
    """

    # make new series with 0s
    comp_df = pd.DataFrame(index=df.index)
    comp_df['spots'] = 0

    filter_df = df[df >= min_depth]
    filter_df = filter_df.dropna(how='any')

    percent = len(filter_df.index) / len(df.index)

    return filter_df, percent


def loci(filter_df):
    """Take filter_df and return a list of loci where bp depth is adequate

    input
    -----
    filter_df = DataFrame

    returns
    -------
    loci - int list
    """
    loci = list(filter_df.index.values)

    return loci


def main():
    #output = input("give output file name: ")
    min_depth = int(input("give min depth: "))

    df, percent = compare(import_reads(), min_depth)

    print(percent)

    print(loci(df))
    # df.to_csv(output)


# ======================== #
#           Main           #
# ======================== #


if __name__ == '__main__':
    main()
