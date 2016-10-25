#PBS -S /bin/bash
#PBS -q batch
#PBS -N vcf_table_test
#PBS -l nodes=1:ppn=8
#PBS -l mem=20
#PBS -l walltime=96:00:00
#PBS -M jacobcfuller93@gmail.com
#PBS -m ae
#PBS -j oe

#first test selection of sample from joint genotype for table
#second test select only SNPs of all samples for table

cd /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/bam/PaxtonBenthicAlignment/

module load java/jdk1.8.0_20 \n
module load picard/2.4.1 \n


#first

java -jar /usr/local/apps/gatk/3.4.0/GenomeAnalysisTK.jar \\
-T SelectVariants \\
-R /lustre1/jcfuller/Stickleback_Genomes_Project/doc/ref/revisedAssemblyUnmasked.fa
-V /lustre1/jcfuller/Stickleback_Genomes_Project/data/genome/bam/PaxtonBenthicAlignment/paxton_JG.vcf_table_test
-o single_sample_test.vcf
-sn male9

java -jar /usr/local/apps/gatk/3.4.0/GenomeAnalysisTK.jar \\
-T VariantsToTable \\
-R /lustre1/jcfuller/Stickleback_Genomes_Project/doc/ref/revisedAssemblyUnmasked.fa \\
-V single_sample_test.vcf \\
-F POS -GF GT -GF PL -GF GQ \\
-o single_sample_test.table
