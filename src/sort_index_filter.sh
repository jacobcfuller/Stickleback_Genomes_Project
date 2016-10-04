#!/bin/bash

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

cd /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/bam/PaxtonBenthicAlignment


module load samtools/latest

#Sort, index
samtools sort -o ${sample}_sorted.bam -T ${sample}_s ${sample}.bam
mv ${sample}_sorted.bam ${sample}.bam
samtools index -b ${sample}.bam

# Filter by whether MAPQ score ≥ 20
samtools view -bh -q 20 ${sample}.bam > ${sample}_q.bam
samtools index -b ${sample}_q.bam
