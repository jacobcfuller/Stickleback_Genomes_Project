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

samtools view -b ${sample}_q.bam chrXIX | \
bedtools genomecov \
  -d \
  -ibam stdin | \
  awk '{print $3}' >> ${sample}_XIX.txt

sleep 1s
echo ${sample}_XIX | tr ' ' '\t' | gzip > ${sample}_XIX.txt.gz
paste ${sample}_XIX.txt | gzip >> ${sample}_XIX.txt.gz
