#PBS -S /bin/bash
#PBS -q batch
#PBS -N jointGeno_JM
#PBS -l nodes=1:ppn=8
#PBS -l mem=20
#PBS -l walltime=96:00:00
#PBS -m ae
#PBS -j oe


cd /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/fastq/feulner/Ca_L


/lustre1/jcfuller/Stickleback_Genomes_Project/bin/GATKpipe/GATKpipe.py jointGeno \
  -o Ca_L\
  -c 8 \
  -r /lustre1/jcfuller/Stickleback_Genomes_Project/doc/ref/revisedAssemblyUnmasked.fa \
  BS44/BS44_q_cV.g.vcf \
  BS46/BS46_q_cV.g.vcf \
  BS48/BS48_q_cV.g.vcf \
  BS50b/BS50b_q_cV.g.vcf \
  BS52b/BS52b_q_cV.g.vcf \
  BS54/BS54_q_cV.g.vcf 
