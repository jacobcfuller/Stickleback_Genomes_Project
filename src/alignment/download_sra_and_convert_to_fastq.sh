#!/bin/bash

unset accession

# Retrieve SRA accession # from command line argument
while getopts ":a:" opt; do
  case $opt in
    a)
      export accession=$OPTARG
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

# Root directory for SRA database
export ftproot=ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra

# Format SRA accession file and download
  pre="${accession:0:3}"
  mid="${accession:0:6}"
  wget ${ftproot}/${pre}/${mid}/${accession}/${accession}.sra

#Convert .sra files to gzipped fastq files
fastq-dump --split-files --gzip ${accession}.sra
