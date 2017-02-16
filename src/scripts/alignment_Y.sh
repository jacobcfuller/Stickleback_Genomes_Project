#!/bin/bash

export mapFilter=true

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


# Align
export read1_list=`ls -m *_1.fastq.gz | tr -d ' \n'`
module load bowtie2/latest
shopt -s nullglob
set -- *_2.fastq.gz
if [ "$#" -gt 0 ]
  then
      export read2_list=`ls -m *_2.fastq.gz | tr -d ' \n'`
      bowtie2 -p 8 --no-unal --very-sensitive -x /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/bowtie/Glazer_unmasked_Y/glazerWithY_unmasked\
      -1 ${read1_list} \
      -2 ${read2_list} \
      -S ${sample}.sam \
      >& ${sample}_summary.txt

  else
      bowtie2 -p 8 --no-unal --very-sensitive -x /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/bowtie/Glazer_unmasked_Y/glazerWithY_unmasked\
      -U ${read1_list} \
      -S ${sample}.sam \
      >& ${sample}_summary.txt
fi
module load samtools/latest
# Sort, index
samtools view -bh -q 30 -@ 7 ${sample}.sam > ${sample}_y.bam
samtools sort -o ${sample}_sorted.bam -T ${sample}_s -@ 8 ${sample}_y.bam
mv ${sample}_sorted.bam ${sample}_y.bam
samtools index -b ${sample}_y.bam

#make depth file
module load bedtools/2.24.0
samtools view -@ 8 -b ${sample}_y.bam PGA_scaffold0__28_contigs__length_12341907 | \
bedtools genomecov \
  -d \
  -ibam stdin | \
  awk '{print $3}' >> ${sample}_Y_depth.txt

sleep 1s
echo ${sample}_Y| tr ' ' '\t' | gzip > ${sample}_Y_depth.txt.gz
paste ${sample}_Y_depth.txt | gzip >> ${sample}_Y_depth.txt.gz

# coverage
bedtools genomecov -ibam ${sample}_y.bam > ${sample}_genome.cov
