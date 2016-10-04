#!/bin/bash

# Retrieve sample from arg
while getopts ":s:d:" opt; do
  case $opt in
    s)
      export sample=$OPTARG
      ;;
    d)
      export dir=$OPTARG
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

module load samtools/latest

total=$(samtools view -c ${sample}.bam)
XIX=$(samtools view -c ${sample}.bam chrXIX)

autosome_count=$((total-XIX))

echo ${sample} ${autosome_count} >> read_count.txt
