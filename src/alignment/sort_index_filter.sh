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

cd /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/feulner/${sample}

module load samtools/latest
# Sort, index
samtools view -bh -q 30 -@ 7 ${sample}.sam > ${sample}_y.bam
samtools sort -o ${sample}_sorted.bam -T ${sample}_s -@ 8 ${sample}_y.bam
mv ${sample}_sorted.bam ${sample}_y.bam
samtools index -b ${sample}_y.bam
