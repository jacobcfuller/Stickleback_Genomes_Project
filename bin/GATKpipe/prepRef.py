"""Prepare reference fasta for GATK pipeline."""


import base
import subprocess as sp
from __main__ import args

'''
import subprocess as sp
sp.call('cd ~/uga/Python/GATKpipe && scp prepRef.py base.py \
lan@xfer2.gacrc.uga.edu:~/tools/GATKpipe', shell = True)
'''

# =====================
#  Reading the arguments from `args`
# =====================

reference = args['reference']


# =====================
# `main` function to run 
# command on all file(s)
# =====================

def main():
    sp.call(base.prepRef % reference, shell = True)