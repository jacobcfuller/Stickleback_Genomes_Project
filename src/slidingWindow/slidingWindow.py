#!/home/jcfuller/anaconda3/bin/python3.5

import pandas
import subprocess
import argparse


# Set up parser
ScriptDescript = '''Sliding Window function on SNP calls'''
Parser = argparse.ArgumentParser(description=ScriptDescript)
Parser.add_argument('-w', '--window', type=int, metavar='W', required=False, default=500,
                    help='Length of the sliding window')
Parser.add_argument('-i', '--increment', type=int, metavar='I', required=False, default=250,
                    help='Increment by which to slide window')
Parser.add_argument('file', type=str, metavar='F')

# Read args
args = vars(Parser.parse_args())

# make objects from args
window = args['window']
incr = args['increment']
file = args['file']
del args




