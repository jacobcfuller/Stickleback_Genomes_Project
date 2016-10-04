"""Base functions for running GATK pipeline on DNA-seq data."""


from multiprocessing import Pool
import subprocess as sp

# ==========================================
#        Functions
# ==========================================

def cleanRun(commandString, logFile, workingDir = '.', logOpenMode = 'at',
             logPrefix = ''):

    """Run command from string and save output to log file."""

    try:
        std = sp.check_output(commandString, cwd = workingDir,
                              shell = True, stderr = sp.STDOUT,
                              universal_newlines = True)
    except sp.CalledProcessError as e:
        std = "command '{}' return with error (code {}):\n{}".format(
            e.cmd, e.returncode, e.output)

    with open(logFile, logOpenMode) as f:
        f.write(logPrefix + std)

    return


def poolRunFun(function, cores, inerable):

    """Run function via Pool or for-loop, depending on # cores; plus allow 2D `inerable`.
    Note: `inerable` is an input iterable (see what I did there?!)."""

    assert cores > 0 and 'int' in str(cores.__class__), \
        '`cores` must be a positive integer.'

    try:
        twoD = inerable[0].__class__ in [list, tuple]
    except TypeError as t:
        if t.args[0] == "'zip' object is not subscriptable":
            twoD = inerable.__class__ == zip
        else:
            raise NotImplementedError(
                'Only 2D list, tuple, or zip objects are implemented.')

    if cores > 1:
        if twoD:
            with Pool(processes = cores) as pool:
                pool.starmap(function, inerable)
        else:
            with Pool(processes = cores) as pool:
                pool.map(function, inerable)
    else:
        if twoD:
            for i in inerable:
                function(*i)
        else:
            for i in inerable:
                function(i)
    return



def splitPath(filePath):

    """Split file's path into filename and directory.

    Note: Allows for just filename given as input when that file is already in the
        current working directory. The returned object `directory` will be simply '.'.
    """

    directory = '/'.join(filePath.split('/')[:-1])

    if len(directory) == 0:
        directory = '.'

    filename = filePath.split('/')[-1]

    return directory, filename


def makeCoreStringList(cores, files, parType):

    """Make list of 'core strings' for multithreading commands, plus adjust `cores`."""

    if cores > len(files):
        coreList = [(cores // len(files)) + 1] * (cores % len(files)) + \
                   [cores // len(files)] * (len(files) - (cores % len(files)))
        coresAdj = len(files)
    else:
        coreList = [1] * len(files)
        coresAdj = cores

    def makeCoreString(numCores, pT):
        """Inner function to create one individual string."""
        if numCores == 1:
            return ''
        else:
            return '-%s %i ' % (pT, numCores)

    coreStrList = [makeCoreString(x, parType) for x in coreList]

    return coreStrList, coresAdj



# ==========================================
#        Command strings
# ==========================================

prepRef = \
'''export ref=%s
export dictOut=`echo ${ref} | sed 's/.fasta$/.dict/g; s/.fa$/.dict/g'`

export javMem=2

module load java/jdk1.8.0_20
module load samtools/1.2
module load picard/2.4.1\n

samtools faidx ${ref}\n

java -Xmx${javMem}g -jar /usr/local/apps/picard/2.4.1/picard.jar \\
CreateSequenceDictionary \\
REFERENCE=${ref} \\
OUTPUT=${dictOut}
'''


addRG = \
'''export bamFile=%(bam)s

export javMem=2

module load java/jdk1.8.0_20
module load samtools/1.2
module load picard/2.4.1\n

java -Xmx${javMem}g \\
    -classpath "/usr/local/apps/picard/2.4.1" \\
    -jar /usr/local/apps/picard/2.4.1/picard.jar \\
    AddOrReplaceReadGroups \\
    CREATE_INDEX=false \\
    INPUT=${bamFile} \\
    OUTPUT=${bamFile/.bam/_rG.bam} \\
    RGID=LANE1 \\
    RGLB=${bamFile/.bam/} \\
    RGPL=ILLUMINA \\
    RGPU=ILLUMINA \\
    RGSM=${bamFile/.bam/}

samtools index -b ${bamFile/.bam/_rG.bam}
'''


markDups = \
'''export bamFile=%(bam)s

export javMem=18

# Making new name, assuming input BAM matches *_<suffix>.bam
# I did it this way so <suffix> can be anything; '_' is only thing that's important.
tmp=(${bamFile//_/ })
unset "tmp[${#tmp[@]}-1]"
export outFile=`echo -n ${tmp[@]} | tr ' ' '_'`_mD.bam\n

module load java/jdk1.8.0_20
module load samtools/1.2
module load picard/2.4.1\n

mkdir ./tmp/${bamFile/.bam/}\n

java -Xmx${javMem}g -Djava.io.tmpdir=./tmp/${bamFile/.bam/} \\
    -classpath "/usr/local/apps/picard/2.4.1" \\
    -jar /usr/local/apps/picard/2.4.1/picard.jar MarkDuplicates \\
    CREATE_INDEX=false \\
    INPUT=${bamFile} \\
    OUTPUT=${outFile} \\
    MAX_RECORDS_IN_RAM=500000 \\
    TMP_DIR=./tmp/${bamFile/.bam/} \\
    METRICS_FILE=${outFile/.bam/.txt}

samtools index -b ${outFile}
'''


reIndels = \
'''export bamFile=%(bam)s
export reference=%(ref)s\n

# Making new name, assuming input BAM matches *_<suffix>.bam
# I did it this way so <suffix> can be anything; '_' is only thing that's important.
tmp=(${bamFile//_/ })
unset "tmp[${#tmp[@]}-1]"
export outFile=`echo -n ${tmp[@]} | tr ' ' '_'`_rI.bam\n

module load java/jdk1.8.0_20
module load samtools/1.2
module load gatk/3.6\n

java -jar /usr/local/apps/gatk/3.6/GenomeAnalysisTK.jar \\
-T RealignerTargetCreator \\
-R ${reference} \\
%(corS)s\\
-I ${bamFile} \\
-o ${outFile/.bam/.list}\n

java -jar /usr/local/apps/gatk/3.6/GenomeAnalysisTK.jar \\
-T IndelRealigner \\
-R ${reference} \\
-I ${bamFile} \\
-targetIntervals ${outFile/.bam/.list} \\
-o ${outFile}\n

samtools index -b ${outFile}
'''


callVariants = \
'''export bamFile=%(bam)s
export reference=%(ref)s\n

# Making new name, assuming input BAM matches *_<suffix>.bam
# I did it this way so <suffix> can be anything; '_' is only thing that's important.
tmp=(${bamFile//_/ })
unset "tmp[${#tmp[@]}-1]"
export outFile=`echo -n ${tmp[@]} | tr ' ' '_'`_cV.g.vcf\n

module load java/jdk1.8.0_20
module load gatk/3.6\n

java -jar /usr/local/apps/gatk/3.6/GenomeAnalysisTK.jar \\
-T HaplotypeCaller \\
-R ${reference} \\
%(corS)s\\
-I ${bamFile} \\
--emitRefConfidence GVCF \\
--genotyping_mode DISCOVERY \\
-o ${outFile}
'''


jointGeno = \
'''export reference=%(ref)s

module load java/jdk1.8.0_20
module load gatk/3.6\n

java -jar /usr/local/apps/gatk/3.6/GenomeAnalysisTK.jar \\
-T GenotypeGVCFs \\
-R ${reference} \\
%(coreS)s \\
%(varS)s \\
%(moreOpts)s \\
-o %(out)s_jG.vcf'''
