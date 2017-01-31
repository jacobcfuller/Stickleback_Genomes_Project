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

samtools view -b ${sample}.bam PGA_scaffold0__28_contigs__length_12341907 | \
bedtools genomecov \
  -d \
  -ibam stdin | \
  awk '{print $3}' >> ${sample}_Y_depth.txt

sleep 1s
echo ${sample}_Y_depth | tr ' ' '\t' | gzip > ${sample}_Y_depth.txt.gz
paste ${sample}_Y_depth.txt | gzip >> ${sample}_Y_depth.txt.gz

mv ${sample}_Y_depth.txt.gz /Volumes/MW_18TB/Jacob_Fuller/snps/depth
