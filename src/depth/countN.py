#!/home/jcfuller/anaconda3/bin/python3.6

# Find # of Ns in .fa files

import fileinput
import sys


def count_N():
    '''Counts 'N' occurences  in .fa files
    '''
    N_count = 0
    for line in fileinput.input():
        for nuc in line.strip():
            if nuc == 'N':
                N_count += 1
    return(N_count)


def find_reg():
    '''Finds substrings of N and returns tuple list of (first, last) indices of
    these regions
    '''
    pos = 0
    first, last = 0, 0
    N_spots = []

    file_path = sys.argv[1]

    with open(file_path) as fa_file:
        # get rid of ">PGA..." part
        chr_start = fa_file.readline()
        seq = fa_file.read()
        seq = seq.replace("\n", "")

        N = False
        for index, nuc in enumerate(seq):
            if nuc == "N" and N is False:
                N = True
                first = index

            if nuc != "N" and N is True:
                last = index - 1
                N = False
                N_spots.append((first, last))

    return(N_spots)


def to_table(N_spots):
    print("Total N Count: " + str(count_N()) + '\n')
    print("Regions \n")
    for spot in N_spots:
        print(spot)


to_table(find_reg())
