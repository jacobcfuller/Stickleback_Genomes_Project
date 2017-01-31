#!/home/jcfuller/anaconda3/bin/python3.5

import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='snp table')
parser.add_argument('file', metavar='F', type=str, help='path to file')
args = vars(parser.parse_args())

dataFile = args['file']

snpDF = pd.read_table(dataFile, delimiter='\t', index_col=0)

ax = snpDF.plot(figsize=(15, 5))
plt.xlabel('Y pos(bp)', size=12)
plt.ylabel('SNP #', size=12)
plt.legend(loc='best')
plt.title(dataFile[:(len(dataFile)-4)]+' 1000bp Sliding Window Count', size=12)
plt.autoscale(axis='x', tight=True)
plt.savefig(dataFile[:(len(dataFile)-4)]+".pdf",
            format='pdf',
            bbox_inches='tight')
