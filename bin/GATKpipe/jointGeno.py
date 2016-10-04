"""Perform joint genotyping on gVCF files via GenotypeGVCFs.

Required ~ 3gb RAM per thread.

Takes around 10-20 minutes."""



import base
from __main__ import args


# =====================
# Reading the arguments from `args`
# =====================

ref = args['reference']
outName = args['outputName']
cores = args['cores']
moreOpts = args['moreOptions'].strip()
files = args['files']
if files.__class__ == str:
    files = [files]

assert ref.endswith('.fa') or ref.endswith('.fasta'), \
    'Reference is not an uncompressed fasta file.'

assert all([x.endswith('.g.vcf') for x in files]), \
    'Not all input files are gVCF files.'



# =====================
# Making cores list
# =====================

# `GenotypeGVCFs` allows multithreading, but if we specify 1 core, we'll skip the 
# `-nt` argument altogether.

if cores > 1:
    coreString = ''
else:
    coreString = '-nt %i' % cores


# =====================
# Making variant list
# =====================


varString = '--variant %s' % ' \\\n--variant '.join(files)



# =====================
# Function to run command
# =====================

def runJointGeno(filePath):
    
    """Run command to do joint genotyping on gVCF files."""
    
    directory, filename = base.splitPath(filePath)
    
    command = base.jointGeno % {'varS': varString, 'ref': ref, 'coreS': coreString, 
                                'out': filename, 'moreOpts': moreOpts}
    
    logFileName = filePath + '_jG.log'
    
    # Run command and save output to log file
    base.cleanRun(commandString = command, logFile = logFileName,
                  workingDir = directory, logOpenMode = 'wt')
    
    return



# =====================
# `main` function to run 
# command on all file(s)
# =====================

def main():
    runJointGeno(outName)


