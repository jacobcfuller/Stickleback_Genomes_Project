#!/bin/bash

unset sample

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

cd /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/${dir}/${sample}

module load samtools/1.2
#bedtools v. 2.25.0 causes weird issues
module unload bedtools/2.25.0
module load bedtools/2.24.0

samtools view -@ 2 -b ${sample}_q.bam PGA_scaffold0__28_contigs__length_12341907 | \
bedtools genomecov \
  -d \
  -ibam stdin | \
  awk '{print $3}' >> ${sample}_Y_depth.txt

sleep 1s
echo ${sample}_Y | tr ' ' '\t' | gzip > ${sample}_Y.txt.gz
paste ${sample}_Y_depth.txt | gzip >> ${sample}_Y.txt.gz
