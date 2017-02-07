#!/bin/bash

unset accession

# Retrieve SRA accession # from command line argument
while getopts ":i:d:a:" opt; do
  case $opt in
    a)
      export accession=$OPTARG
      ;;
    d)
      export dir=$OPTARG
      ;;
    i)
      export ind=$OPTARG
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

cd /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/feulner/${dir}/${ind}

# Root directory for SRA database
export ftproot=ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra

# Format SRA accession file and download
  pre="${accession:0:3}"
  mid="${accession:0:6}"
  wget ${ftproot}/${pre}/${mid}/${accession}/${accession}.sra

module load sratoolkit/latest
#Convert .sra files to gzipped fastq files
fastq-dump --split-files --gzip ${accession}.sra
