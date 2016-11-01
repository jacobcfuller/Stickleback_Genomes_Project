#!/bin/bash

export cores=12

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

cd /lustre1/jcfuller/stick/genome/bam

# Sort, index
module load samtools/latest

samtools sort -o ${sample}_sorted.bam -T ${sample}_s -@ ${cores} ${sample}.bam
mv ${sample}_sorted.bam ${sample}.bam
samtools index -b ${sample}.bam


samtools view -bh -q 20 -@ $(expr ${cores} - 1) ${sample}.bam > ${sample}_q.bam
samtools index -b ${sample}_q.bam
