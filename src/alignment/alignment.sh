#!/bin/bash

export mapFilter=true

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

# Align
export read1_list=`ls -m *_1.fastq.gz | tr -d ' \n'`
module load bowtie2/latest
shopt -s nullglob
set -- *_2.fastq.gz
if [ "$#" -gt 0 ]
  then
      export read2_list=`ls -m *_2.fastq.gz | tr -d ' \n'`
      bowtie2 -p 8 --no-unal --very-sensitive -x /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/bowtie/Glazer/Glazer \
      -1 ${read1_list} \
      -2 ${read2_list} \
      -S ${sample}.sam \
      >& ${sample}_summary.txt

  else
      bowtie2 -p 8 --no-unal --very-sensitive -x /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/bowtie/Glazer/Glazer \
      -U ${read1_list} \
      -S ${sample}.sam \
      >& ${sample}_${runNum}_summary.txt
fi
module load samtools/latest
# Sort, index
samtools view -bh -@ 8 ${sample}.sam > ${sample}.bam
samtools sort -o ${sample}_sorted.bam -T ${sample}_s -@ 8 ${sample}.bam
mv ${sample}_sorted.bam ${sample}.bam
samtools index -b ${sample}.bam

# Filter by whether MAPQ score ≥ 30
if [ ${mapFilter} = true ]
then
    samtools view -bh -q 30 -@ 8 ${sample}.bam > ${sample}_q.bam
    samtools index -b ${sample}_q.bam
fi
