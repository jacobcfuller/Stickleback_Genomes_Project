# Read Depth Data Analysis - Y Chromosome
### Goals:
* Discover/characterize population level structural variation on the Y Chromosome using read depth to find duplications/deletions.

# Current Pipeline
## Acquiring data & preprocessing:
* Identify available, high quality whole genome sequences on SRA database. Ideally > 10x coverage. Paired end.
* Download SRA files onto UGA's lustre drive.
* Convert SRA to fastq, separating pairs
```bash
module load sratoolkit/latest
#Convert .sra files to gzipped fastq files
fastq-dump --split-files --gzip ${accession}.sra
```
* Align using Bowtie2.
```bash
bowtie2 -p 8 --no-unal --very-sensitive -x unmasked_glazer_with_Y.fa \
      -1 ${read1_list} \
      -2 ${read2_list} \
      -S ${sample}.sam \
      >& ${sample}_summary.txt
```
* Convert .sam to .bam using samtools
* Sort with samtools sort
* Index with samtools index
```bash
samtools view -bh -q 30 -@ 8 ${sample}.sam > ${sample}.bam
samtools sort -o ${sample}_sorted.bam -T ${sample}_s -@ 8 ${sample}.bam
mv ${sample}_sorted.bam ${sample}.bam
samtools index -b ${sample}.bam
```
* Filter based on map quality of 30 (samtools). This may change.
* Use bedtools to retrieve read depth at each base pair
```bash
module load bedtools/2.24.0
samtools view -@ 8 -b t_${sample}_y.bam PGA_scaffold0__28_contigs__length_12341907 | \
bedtools genomecov \
  -d \
  -ibam stdin | \
  awk '{print $3}' >> t_${sample}_Y_depth.txt
```
* Also, get # of reads for the genome
```bash
bedtools genomecov -ibam ${sample}_y.bam > ${sample}_genome.cov
```
