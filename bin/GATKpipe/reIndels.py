"""Local realignment around indels via GATK RealignerTargetCreator and IndelRealigner.

Requires ~15gb RAM per thread for mice AND stickleback.

Takes from ~12 hrs to 2 days.
"""


import base
from __main__ import args


# =====================
# Reading the arguments from `args`
# =====================

ref = args['reference']
cores = args['cores']
files = args['files']
if files.__class__ == str:
    files = [files]

assert ref.endswith('.fa') or ref.endswith('.fasta'), \
    'Reference is not an uncompressed fasta file.'

assert all([x.endswith('.bam') or x.endswith('.BAM') for x in files]), \
    'Not all input files are BAM files.'

assert cores > 0 and 'int' in str(cores.__class__), '`cores` must be an integer > 0.'


# =====================
# Making cores list
# =====================

# Because `RealignerTargetCreator` allows multithreading for a single sample, we've add 
# the ability to specify more cores than samples, which will be passed to that step.

# For sample(s) that get 1 core, we'll skip the `-nt` argument altogether.

# Also have to adjust `cores` object for Pool function if it's larger than # files 

coreStrList, cores = base.makeCoreStringList(cores, files, 'nt')




# =====================
# Function to run command
# =====================

def runReIndels(filePath, coreString):
    
    """Run command to do local realignment around indels on BAM file."""
    
    directory, filename = base.splitPath(filePath)
    
    command = base.reIndels % {'bam': filename, 'ref': ref, 'corS': coreString}
    
    logFileName = '_'.join(filePath.split('_')[:-1] + ['rI.log'])
    
    # Run command and save output to log file
    base.cleanRun(commandString = command, logFile = logFileName,
                  workingDir = directory, logOpenMode = 'wt')
    
    return


# =====================
# `main` function to run 
# command on all file(s)
# =====================

def main():
    base.poolRunFun(function = runReIndels, cores = cores, 
                    inerable = zip(files, coreStrList))



