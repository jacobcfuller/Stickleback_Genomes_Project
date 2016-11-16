#!/bin/bash

export mapFilter=true

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

# Align
export read1_list=`ls -m *_1.fastq.gz | tr -d ' \n'`

shopt -s nullglob
set -- *_2.fastq.gz
if [ "$#" -gt 0 ]
  then
      export read2_list=`ls -m *_2.fastq.gz | tr -d ' \n'`
      bowtie2 --no-unal --very-sensitive -x /escratch4/jcfuller/jcfuller_Nov_15/Glazer \
      -1 ${read1_list} \
      -2 ${read2_list} \
      -S ${sample}.sam \
      >& ${sample}_summary.txt

  else
      bowtie2 --no-unal --very-sensitive -x /escratch4/jcfuller/jcfuller_Nov_15/Glazer \
      -U ${read1_list} \
      -S ${sample}.sam \
      >& ${sample}_${runNum}_summary.txt
fi

# Sort, index
samtools view -bh ${sample}.sam > ${sample}.bam
samtools sort -o ${sample}_sorted.bam -T ${sample}_s  ${sample}.bam
mv ${sample}_sorted.bam ${sample}.bam
samtools index -b ${sample}.bam

# Filter by whether MAPQ score ≥ 20
if [ ${mapFilter} = true ]
then
    samtools view -bh -q 20 ${sample}.bam > ${sample}_q.bam
    samtools index -b ${sample}_q.bam
fi
