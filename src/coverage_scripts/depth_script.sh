#!/bin/bash

# Retrieve sample from arg
while getopts ":s:c:n:" opt; do
  case $opt in
    s)
      export sample=$OPTARG
      ;;
    c)
      export chr_num=$OPTARG
      ;;
    n)
      export name=$OPTARG
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

samtools view -b ${sample}.bam chr${chr_num} | \
bedtools genomecov \
  -d \
  -ibam stdin | \
  awk '{print $3}' >> ${sample}_${chr_num}_depth.txt

sleep 1s
echo ${name}_${chr_num} | tr ' ' '\t' | gzip > ${name}_${chr_num}.txt.gz
paste ${sample}_${chr_num}_depth.txt | gzip >> ${name}_${chr_num}.txt.gz
