#!/bin/bash

unset sample

# Retrieve sample from arg
while getopts ":s:" opt; do
  case $opt in
    s)
      export sample=$OPTARG
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

cd /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/bam/japan_sea/male/

module load samtools/1.2
#bedtools v. 2.25.0 causes weird issues
module unload bedtools/2.25.0
module load bedtools/2.24.0

samtools view -b ${sample}.bam chrXIX | \
bedtools genomecov \
  -d \
  -ibam stdin | \
  awk '{print $3}' >> ${sample}_XIX_depth.txt

sleep 1s
echo ${sample}_XIX | tr ' ' '\t' | gzip > ${sample}_XIX.txt.gz
paste ${sample}_XIX_depth.txt | gzip >> ${sample}_XIX.txt.gz
