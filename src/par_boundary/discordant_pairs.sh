#PBS -S /bin/bash
#PBS -q batch
#PBS -N discordant_BS64b
#PBS -l nodes=1:ppn=2
#PBS -l mem=4gb
#PBS -l walltime=96:00:00
#PBS -m ae
#PBS -j oe


cd /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/fastq/feulner/No_L/BS64b


module load samtools/latest
# Extract discordant paired-end alignments.
samtools view BS64b.bam "chrXIX" -b -F 1294 > BS64b.discordants.unsorted.bam

samtools sort BS64b.discordants.unsorted.bam BS64b.discordants
