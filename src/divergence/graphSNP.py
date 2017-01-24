#!/home/jcfuller/anaconda3/bin/python3.5

import argparse
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='snp table')
parser.add_argument('file', metavar='F', type=str, help='path to file')
args = vars(parser.parse_args())

dataFile = args['file']

snpDF = pd.read_table(dataFile, delimiter='\t')

plt.figure(num=1, figsize=(15, 5))
plt.bar(left=snpDF['pos'],
        width=0.1,
        height=snpDF['snp #'],
        color='r')
plt.xlabel('Y pos(bp)', size=12)
plt.ylabel('SNP #', size=12)
plt.title(dataFile[:(len(dataFile)-4)]+' 1000bp Sliding Window Count', size=12)
plt.autoscale(axis='x', tight=True)
plt.savefig(dataFile[:(len(dataFile)-4)]+".pdf",
            format='pdf',
            bbox_inches='tight')
