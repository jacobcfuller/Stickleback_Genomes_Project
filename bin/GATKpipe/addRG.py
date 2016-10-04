"""Add read groups to bam files using PICARD AddOrReplaceReadGroups.

9 cores used 5.870788 Gb RAM and took 1 hr, 13 min."""


import base
from __main__ import args


# =====================
# Reading the arguments from `args`
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

def runAddRG(filePath):
    
    """Run command to add read groups to BAM file and index new one."""
    
    directory, filename = base.splitPath(filePath)
    
    command = base.addRG % {'bam': filename}
    
    logFileName = filePath.replace('.bam', '_rG.log')
    
    # Run command and save output to log file
    base.cleanRun(commandString = command, logFile = logFileName,
                  workingDir = directory, logOpenMode = 'wt')
    
    return




# =====================
# `main` function to run 
# command on all file(s)
# =====================

def main():
    base.poolRunFun(function = runAddRG, cores = cores, inerable = files)


