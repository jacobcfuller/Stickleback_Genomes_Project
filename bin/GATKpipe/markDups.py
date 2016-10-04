"""Mark duplicates in BAM files via PICARD MarkDuplicates.

Note: Multithreaded is only useful if you have tons of RAM (>=20 GB per thread). It may
be easiest to run an array job.

Uses ~20GB per thread, and took around 3 hrs for castaneus sample "castEiJ", which had 
an 18GB BAM file.
"""


import base
from __main__ import args


# =====================
# Reading the arguments
# =====================

cores = args['cores']
files = args['files']
if files.__class__ == str:
    files = [files]

assert all([x.endswith('.bam') or x.endswith('.BAM') for x in files]), \
    'Not all input files are BAM files.'



# =====================
# Function to run command once
# =====================

def runMarkDups(filePath):
    
    """Run command to mark duplicates in BAM file."""
    
    directory, filename = base.splitPath(filePath)
    
    command = base.markDups % {'bam': filename}
    
    logFileName = '_'.join(filePath.split('_')[:-1] + ['mD.log'])
    
    # Run command and save output to log file
    base.cleanRun(commandString = command, logFile = logFileName,
                  workingDir = directory, logOpenMode = 'wt')
    return



# =====================
# `main` function to run 
# command on all file(s)
# =====================

def main():
    base.poolRunFun(function = runMarkDups, cores = cores, inerable = files)



