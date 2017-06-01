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
    """Examine read depth at each bp position. If shared between all
    individuals, add "1" to new df, else add "0".

    input
    -----
    df - DataFrame from import_reads()
    min_depth - int value representing minimum allowable read depth for
                analysis

    returns
    -------
    comp_df - DataFrame of 1/0 where 1 represents a bp that can be analyzed
    """

    # make new series with 0s
    comp_df = pd.DataFrame(index=df.index)
    comp_df['spots'] = 0

    filter_df = df[df >= min_depth]
    filter_df = filter_df.dropna(how='any')

    percent = len(filter_df.index) / len(df.index)

    return filter_df, percent


def main():
    output = input("give output file name: ")
    min_depth = input("give min depth: ")

    df = compare(import_reads(), min_depth)

    df.to_csv(output)


# ======================== #
#           Main           #
# ======================== #


if __name__ == '__main__':
    main()
