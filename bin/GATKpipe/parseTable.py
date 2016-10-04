#!/usr/local/apps/anaconda/3-2.2.0/bin/python

"""Output filtered, plottable table from VariantsToTable output.

Extract specific fields for all samples from a VCF file to a tab-delimited table.
"""





import argparse as ap
from multiprocessing import Pool
# from time import strftime
import os
import gzip
import pandas as pd

import base as lan


__author__ = 'Lucas Nell'


# Example output from VariantsToTable
'''
[lan@n15 GATK]$ more domD22_19b9.table
POS	D22.GT	D22.PL	D22.GQ
3000093	T/T	0,0,131	0
3000170	G/A	263,0,2504	99
3000188	C/T	1210,0,1790	99
3000201	T/A	1376,0,1537	99
3000216	G/A	1534,0,1972	99
3000261	A/A	0,120,1800	99
3000266	A/C	459,0,2816	99
3000287	T/G	1664,0,1396	99
3000305	G/A	1411,0,1402	99
'''


os.system('cp domD22_Xb9.table testTab.table')


def cleanCols(inTab):
    """Cleans columns names in tables output from GATK's VariantsToTable.

    Example:
        GATK output =     POS   D22.GT    D22.PL    D22.GQ
        'Clean' columns = POS   GT        PL        GQ
        (will be tab-delimited in both; spaces used here for compatibility.)
    """
    tempTab = inTab.replace('.table', '_temp.table')
    with gzip.open(inTab, 'rt') as rf, gzip.open(tempTab, 'wt') as wf:
        for line in rf:
            if line.startswith('POS'):
                headList = line.split()
                for h in range(1, len(headList)):
                    headList[h] = headList[h].split('.')[1]
                newHeads = '\t'.join(headList) + '\n'
                wf.write(newHeads)
            else:
                wf.write(line)
    os.system('mv %s %s' % (tempTab, inTab))
    print('Finished writing new "%s"' % inTab)
    return



def simpGeno(compGeno):
    """Simplies genotypes from strings to simple 0 (homozygous) or 1 (hetero)."""
    compL = compGeno.split('/')
    if compL[0] == compL[1]:
        return 0
    else:
        return 1



def processTab(tabName, dirtyCols = False):
    """Clean and process a VariantsToTable file into a simple table for plotting.
    """
    if dirtyCols:
        cleanCols(tabName)
    # Data types
    Types = [('POS', 'int'), ('GT', 'str'), ('PL', 'str'), ('GQ', 'float')]
    newTab = pd.read_table(tabName, dtype = Types)
    newTab = newTab.dropna()
    newTab = newTab.loc[newTab.GQ >= 20, :]
    # Converting this column to ints now, as they're rounded
    # Couldn't input them as ints, bc it has NA's; this is a limitation of pandas
    newTab['GQ'] = newTab['GQ'].astype(int)
    newTab['geno'] = newTab['GT'].apply(simpGeno)
    newTab.to_csv(tabName.replace('.table', '.txt'), sep = '\t',
                  index = False, columns = ('POS', 'geno', 'GQ'),
                  header = ['pos', 'geno', 'gq'],
                  compression = 'gzip')
    # os.system('gzip ' + tabName.replace('.table.gz', '.txt'))
    print('Finished processing\nOutput to ' + tabName.replace('.table', '.txt'))
    return



# Bash command to get these files
'''
cd ~/Desktop
mkdir GATK

for f in \
castH12_19b9.table.gz \
castH12_Xb9.table.gz \
castH15_19b9.table.gz \
castH15_Xb9.table.gz \
castH28_19b9.table.gz \
castH28_Xb9.table.gz \
castH34_19b9.table.gz \
castH34_Xb9.table.gz
do
scp lan@xfer2.gacrc.uga.edu:/lustre1/lan/musDNA/cast/GATK/${f} ~/Desktop/GATK
done

for f in \
domD22_19b9.table.gz \
domD22_Xb9.table.gz \
domD8_19b9.table.gz \
domD8_Xb9.table.gz \
domD9_19b9.table.gz \
domD9_Xb9.table.gz \
domDF_19b9.table.gz \
domDF_Xb9.table.gz
do
scp lan@xfer2.gacrc.uga.edu:/lustre1/lan/musDNA/dom/GATK/${f} ~/Desktop/GATK
done
'''



os.chdir(os.path.expanduser('~/Desktop/GATK'))


tables = [x for x in os.listdir() if x.endswith('.table.gz')]


for t in tables:
    processTab(t)
print('`' * 10, 'TOTALLY DONE', '`' * 10)
os.system('mkdir GATKtabs; mv *txt* ./GATKtabs')



# =============================
# Setting up parser
# =============================

# ScriptDescript = '''Parse VCF file into a tab-delimited table.'''
#
# Parser = ap.ArgumentParser(description = ScriptDescript)
# Parser.add_argument('-d', '--directory',  type = str, metavar = 'D',
#                     help = 'Full path to vcf file(s)', required = True)
# Parser.add_argument('-t', '--threads',  type = int, metavar = 'T',
#                     required = False, default = 1,
#                     help = 'Max # threads to use (default = 1). It is not useful to'+\
#                     ' provide threads > # files passed.')
# Parser.add_argument('fileChrs', type = str, metavar = 'F', nargs = '+',
#                     help = 'vcf file(s) that you would like to split by sample, ' + \
#                         'along with the chromosome it is aligned to, separated by ":". '+\
#                         'Example: "dom_Xb9jG.vcf:Xb9".')




# -----------------------------
# Now reading the arguments
# -----------------------------
# args = vars(Parser.parse_args())
#
# # Changing to vcf directory
# os.chdir(args['directory'])
#
# # Reading other parameters
# vcfFiles = [x.split(':')[0] for x in args['fileChrs']]
# Chrs = [x.split(':')[1] for x in args['fileChrs']]
# maxCores = args['threads']
#
#
# # Assembly files, derived from the chromosome name
# Assemblies = [lan.getAssem(c) for c in Chrs]
#
#
#
#
# def vcfNames(vcfFile):
#     """Extract sample names from a vcf file."""
#     begParts = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']
#     with open(vcfFile, mode = 'rt') as f:
#         for line in f:
#             if line.startswith('#CHROM'):
#                 sampNames = [x for x in line.strip().split('\t') if x not in begParts]
#                 return sampNames
#
#
#
# allSamps = [' -F '.join(vcfNames(x)) for x in vcfFiles]
#


# For testing
# vcfFiles = ['dom_Xb9jG.vcf', 'dom_19b9jG.vcf']
# dct = dict(infile = vcfFiles[0],
#            ref = 'REF GOES HERE',
#            samps = allSamps[0])
# print(str(tabComm % dct))










# if __name__ == '__main__':
#     if maxCores > 1:
#         # start 'maxCores' worker processes
#         with Pool(processes = maxCores) as pool:
#             pool.map(doSelect, range(len(allSamps)))
#     # If it's not in parallel, might as well not use Pool, to avoid overhead
#     else:
#         for j in range(len(allSamps)):
#             doSelect(j)





# os.system('''scp /Users/lucasnell/uga/Python/GATKpipe/parseTable.py \
# lan@xfer2.gacrc.uga.edu:~/GATKpipe''')
