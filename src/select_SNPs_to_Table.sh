#!/bin/bash

# Script to select SNP variants from joint genotype vcf file
# Reads from list of samples from command line arg provided in sapelo sub script

# Retrieve sample, directory, and joint genotype (pop) file from arg
while getopts ":s:d:p:" opt; do
  case $opt in
    s)
      export sample=$OPTARG
      ;;
    d)
      export dir=$OPTARG
      ;;
    p)
      export pop=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

cd /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/bam/${dir}

# Make sure to keep these up to date
module load java/jdk1.8.0_20
module load gatk/3.6

# Select LG XIX from specific sample
java -jar /usr/local/apps/gatk/latest/GenomeAnalysisTK.jar \
-T SelectVariants \
-R /lustre1/jcfuller/Stickleback_Genomes_Project/doc/ref/revisedAssemblyUnmasked.fa \
-V ${pop} \
-o ${sample}_XIX.vcf \
-L chrXIX
-selectType SNP
-sn ${sample}

# Place selected variants into table
java -jar /usr/local/apps/gatk/latest/GenomeAnalysisTK.jar \
-T VariantsToTable \
-R /lustre1/jcfuller/Stickleback_Genomes_Project/doc/ref/revisedAssemblyUnmasked.fa \
-V ${sample}_XIX.vcf \
-F POS -F CHROM -GF GT -GF PL -GF GQ  \
-o ${sample}_XIX.table
