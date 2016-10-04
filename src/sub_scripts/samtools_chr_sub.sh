#PBS -S /bin/bash
#PBS -q batch
#PBS -N chr_XIX
#PBS -l nodes=1:ppn=8
#PBS -l mem=2
#PBS -l walltime=96:00:00
#PBS -M jacobcfuller93@gmail.com
#PBS -m ae
#PBS -j oe


cd /lustre1/jcfuller/stick/genome/bam/pacific_ocean

module load samtools/latest

samtools view -b DRX012542_q.bam chrXIX >> 542_q_XIX.bam
sleep 1s
samtools view -b DRX012544_q.bam chrXIX >> 544_q_XIX.bam
sleep 1s
samtools view -b DRX012547_q.bam chrXIX >> 547_q_XIX.bam
sleep 1s
