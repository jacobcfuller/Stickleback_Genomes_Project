#!/usr/local/apps/anaconda/3-2.2.0/bin/python

"""Select variants with SelectVariants. Extract fields with VariantsToTable.

Select a subset of variants from a larger callset, then extract specific fields from a
VCF file to a tab-delimited table.

Uses 4-9gb RAM per thread.
Takes 5-10 minutes.

"""


'''
import subprocess as sp
sp.call('cd ~/uga/Python/GATKpipe && scp genoTab.py base.py \
lan@xfer2.gacrc.uga.edu:~/tools/GATKpipe', shell = True)
'''

import argparse as ap
import base


# =====================
#  Setting up parser
# =====================
ScriptDescript = 'Select variants with SelectVariants. ' + \
                 'Extract fields with VariantsToTable.'

Parser = ap.ArgumentParser(description = ScriptDescript)
Parser.add_argument('-r', '--reference', metavar = 'R', 
                    help = "Path to uncompressed reference fasta file. It is assumed " + \
                           "that all input VCF files were aligned to this reference.")
Parser.add_argument('-c', '--cores', type = int, metavar = 'C', default = 1, 
                    help = "Maximum number of cores to use. Defaults to 1.")
Parser.add_argument('files', metavar = 'F', nargs = '+',
                    help = 'VCF file(s) that you would like to split by sample.')


# =====================
# Reading the arguments
# =====================
args = vars(Parser.parse_args())
ref = args['reference']
cores = args['cores']
files = args['files']
if files.__class__ == str:
    files = [files]

assert ref.endswith('.fa') or ref.endswith('.fasta'), \
    'Reference is not an uncompressed fasta file.'

assert all([x.endswith('.vcf') or x.endswith('.VCF') for x in files]), \
    'Not all input files are VCF files.'




# {'jointVCF': VCFfile, 'samp': sample, 'ref': reference, 'out': outName}
selTabComm = \
'''export jointVCF=%(jointVCF)s
export samp=%(samp)s
export reference=%(ref)s
outBase=%(out)s\n

module load java/latest\n

java -jar /usr/local/apps/gatk/latest/GenomeAnalysisTK.jar \\
-T SelectVariants \\
-R ${reference} \\
-V ${jointVCF} \\
-o ${outBase}.vcf \\
-sn ${samp}\n

java -jar /usr/local/apps/gatk/latest/GenomeAnalysisTK.jar \\
-T VariantsToTable \\
-R ${reference} \\
-V ${outBase}.vcf \\
-F POS -GF GT -GF PL -GF GQ \\
-o ${outBase}.table

'''

# =====================
# Smaller functions
# =====================

def vcfNames(vcfFile):
    
    """Extract sample names from a vcf file."""
    
    begParts = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']
    
    with open(vcfFile, mode = 'rt') as f:
        for line in f:
            if line.startswith('#CHROM'):
                allCols = line.strip().split('\t')
                sampNames = [x for x in allCols if x not in begParts]
                return sampNames
    return








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
# Run command on all file(s)
# =====================

if __name__ ==  '__main__':
    base.poolRunFun(function = runCallVariants, cores = cores, 
                    inerable = zip(files, coreStrList))































"""

Example submission script.

#PBS -S /bin/bash
#PBS -q batch
#PBS -N toTab_dom
#PBS -l nodes=1:ppn=8:AMD
#PBS -l walltime=10:00:00
#PBS -l mem=80gb
#PBS -M lucnell@gmail.com
#PBS -m ae

export py=${HOME}/GATKpipe/genoTab.py

$py -t 8 -d /lustre1/lan/musDNA/dom/GATK dom_Xb9jG.vcf:Xb9 dom_19b9jG.vcf:19b9
"""


import argparse as ap
from multiprocessing import Pool
import os

import base as lan


__author__ = 'Lucas Nell'


# Basic script
selTabComm = \
'''module load java/jdk1.7.0_67\n

export inFile=%(infile)s
export samp=%(samp)s
export ref=%(ref)s

outBase=%(out)s

java -jar /usr/local/apps/gatk/3.4.0/GenomeAnalysisTK.jar \\
-T SelectVariants \\
-R ${ref} \\
-V ${inFile} \\
-o ${outBase}.vcf \\
-sn ${samp}\n

java -jar /usr/local/apps/gatk/3.4.0/GenomeAnalysisTK.jar \\
-T VariantsToTable \\
-R ${ref} \\
-V ${outBase}.vcf \\
-F POS -GF GT -GF PL -GF GQ \\
-o ${outBase}.table

# gzip ${outBase}.vcf
# gzip ${outBase}.table

'''




# dict(ref = '/lustre1/lan/', infile = '', samp = '')


# =============================
# Setting up parser
# =============================

ScriptDescript = '''Select a subset of variants from a larger callset'''

Parser = ap.ArgumentParser(description = ScriptDescript)
Parser.add_argument('-d', '--directory',  type = str, metavar = 'D',
                    help = 'Full path to vcf file(s)', required = True)
Parser.add_argument('-t', '--threads',  type = int, metavar = 'T',
                    required = False, default = 1,
                    help = 'Max # threads to use (default = 1). It is not useful to'+\
                    ' provide threads > # samples in all files passed.')
Parser.add_argument('fileChrs', type = str, metavar = 'F', nargs = '+',
                    help = 'vcf file(s) that you would like to split by sample, ' + \
                        'along with the chromosome it is aligned to, separated by ":". '+\
                        'Example: "dom_Xb9jG.vcf:Xb9".')




# -----------------------------
# Now reading the arguments
# -----------------------------
args = vars(Parser.parse_args())

# Changing to vcf directory
os.chdir(args['directory'])

# Reading other parameters
vcfFiles = [x.split(':')[0] for x in args['fileChrs']]
Chrs = [x.split(':')[1] for x in args['fileChrs']]
maxCores = args['threads']


# Assembly files, derived from the chromosome name
Assemblies = [lan.getAssem(c) for c in Chrs]



def makeBaseOut(f, s):
    baseOut = f.replace('_', s + '_').replace('jG', '').replace('.vcf', '')
    return baseOut




# So we don't have to run serial within files, I'm making lists of all samples and
# associated files and assemblies; indexes will align

allSamps = []
sampFiles = []
sampAssems = []
allOuts = []


for i in range(len(vcfFiles)):
    samps = vcfNames(vcfFiles[i])
    fls = [vcfFiles[i]] * len(samps)
    assms = [Assemblies[i]] * len(samps)
    outs = [makeBaseOut(x, y) for x,y in zip(fls, samps)]
    allSamps += samps
    sampFiles += fls
    sampAssems += assms
    allOuts += outs




def doSelect(j):
    """Simple function to run command using previously created lists."""
    dct = dict(infile = sampFiles[j],
               samp = allSamps[j],
               ref = sampAssems[j],
               out = allOuts[j]
               )
    Comm = str(selTabComm % dct)
    os.system(Comm)
    return



def cleanVCF(dirtyFile):
    """Gets rid of the unnecessary parts of names for samples.

    Note: must include old naming for chrs, as some were run before new scheme.
    Note 2: This has already been run on dom+cast vcf files, so no need to implement here.
    I kept it around simply for future reference."""
    getRid = ['_Xb9', '_19b9', '_X9', '_19-9', 'dom', 'cast']
    makeTo = [''] * 4 + ['D', '']
    outName = dirtyFile.replace('.vcf', '_clean.vcf')
    with open(dirtyFile, 'rt') as inFile, open(outName, 'wt') as outFile:
        for line in inFile:
            if line.startswith('#CHROM'):
                l = line
                for s in range(len(getRid)):
                    l = l.replace(getRid[s], makeTo[s])
                outFile.write(l)
            else:
                outFile.write(line)
    os.system('mv %s %s' % (outName, dirtyFile))
    return



# f = "dom_Xb9jG.vcf"
# s = vcfNames(f)[0]
# out = f.replace('_', s.split('_')[0].replace(
#     'dom', '').replace('cast', '') + '_').replace('jG', '').replace('.vcf', '')




if __name__ == '__main__':
    if maxCores > 1:
        # start 'maxCores' worker processes
        with Pool(processes = maxCores) as pool:
            pool.map(doSelect, range(len(allSamps)))
    # If it's not in parallel, might as well not use Pool, to avoid overhead
    else:
        for j in range(len(allSamps)):
            doSelect(j)






# os.system('''scp /Users/lucasnell/uga/Python/GATKpipe/genoTab.py \
# lan@xfer2.gacrc.uga.edu:~/GATKpipe''')
