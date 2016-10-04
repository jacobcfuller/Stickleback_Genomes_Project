#PBS -S /bin/bash
#PBS -q batch
#PBS -N sliding_window
#PBS -l nodes=1:ppn=20
#PBS -l mem=20
#PBS -l walltime=96:00:00
#PBS -M jacobcfuller93@gmail.com
#PBS -m ae
#PBS -j oe


cd /lustre1/jcfuller/stick/genome/bam/pacific_ocean

module load anaconda/3-2.2.0

python /home/jcfuller/Stickleback_Genomes_Project/depth_analysis/slidWin.py \
542_XIX_depth.txt.gz
