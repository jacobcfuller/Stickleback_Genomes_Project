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

cd /escratch4/jcfuller/jcfuller_Nov_15/stickleback_fastq/${sample}

samtools view -b ${sample}.bam chrXIX | \
time /usr/local/bedtools/2.24.0/bin/bedtools genomecov \
  -d \
  -ibam stdin | \
  awk '{print $3}' >> ${sample}_XIX_depth.txt

sleep 1s
echo ${sample}_XIX | tr ' ' '\t' | gzip > ${sample}_XIX.txt.gz
paste ${sample}_XIX_depth.txt | gzip >> ${sample}_XIX.txt.gz
