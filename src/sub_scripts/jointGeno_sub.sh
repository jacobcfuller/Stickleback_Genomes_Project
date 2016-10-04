#PBS -S /bin/bash
#PBS -q batch
#PBS -N jointGeno_JM
#PBS -l nodes=1:ppn=12
#PBS -l mem=40
#PBS -l walltime=96:00:00
#PBS -M jacobcfuller93@gmail.com
#PBS -m ae
#PBS -j oe


cd /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/bam/PaxtonBenthicAlignment

/lustre1/jcfuller/Stickleback_Genomes_Project/bin/GATKpipe/GATKpipe.py jointGeno \
  -o paxton\
  -c 8 \
  -r /lustre1/jcfuller/Stickleback_Genomes_Project/doc/ref/revisedAssemblyUnmasked.fa \
  male9_q_cV.g.vcf  male10_q_cV.g.vcf  male11_q_cV.g.vcf  male12_q_cV.g.vcf
