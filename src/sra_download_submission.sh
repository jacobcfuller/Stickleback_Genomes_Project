#PBS -S /bin/bash
#PBS -q batch
#PBS -N sra_download_convert
#PBS -l nodes=1:ppn=48:mwnode
#PBS -l mem=120gb
#PBS -l walltime=96:00:00
#PBS -M jacobcfuller93@gmail.com
#PBS -m ae
#PBS -j oe

fetch=stickleback_run_accessions.txt

arr=()
while read -r line
do
    arr+=("$line")
done < ${fetch}

shell_opt="a:"$(echo ${arr[@]} | sed 's/ /;/g')


./scripts/parallel_bash.py \
    -s ~/scripts/download_sra_and_convert_to_fastq.sh \
    -t 48 \
    ${shell_opt}
