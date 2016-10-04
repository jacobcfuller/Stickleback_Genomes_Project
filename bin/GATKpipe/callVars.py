"""Call variants with HaplotypeCaller.

Requires about ~12gb RAM per thread.

May take 1-2 days.


HaplotypeCaller can be parallel via `-nct ${cores}`, but...
"Many users have reported issues running HaplotypeCaller with the -nct argument, 
so we recommend using Queue to parallelize HaplotypeCaller instead of multithreading."
So be advised...
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



# =====================
# Making cores list
# =====================

# Because `RealignerTargetCreator` allows multithreading for a single sample, we've add 
# the ability to specify more cores than samples, which will be passed to that step.

# For sample(s) that get 1 core, we'll skip the `-nct` argument altogether.

# Also have to adjust `cores` object for Pool function if it's larger than # files 

coreStrList, cores = base.makeCoreStringList(cores, files, 'nct')




# =====================
# Function to run command
# =====================

def runCallVariants(filePath, coreString):
    
    """Run command to call variants on BAM file."""
    
    directory, filename = base.splitPath(filePath)
    
    command = base.callVariants % {'bam': filename, 'ref': ref, 'corS': coreString}
    
    logFileName = '_'.join(filePath.split('_')[:-1] + ['cV.log'])
    
    # Run command and save output to log file
    base.cleanRun(commandString = command, logFile = logFileName,
                  workingDir = directory, logOpenMode = 'wt')
    
    return



# =====================
# `main` function to run 
# command on all file(s)
# =====================

def main():
    base.poolRunFun(function = runCallVariants, cores = cores, 
                    inerable = zip(files, coreStrList))

