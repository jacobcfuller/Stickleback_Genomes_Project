#!/bin/bash

while getopts ":s:d:p:" opt; do
  case $opt in
    s)
      export sample=$OPTARG
      ;;
    d)
      export dir=$OPTARG
      ;;
    p)
      export pop=$OPTARG
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

while read -r line
do

$(cat << EOF > /home/jcfuller/sub_scripts/select_SNPs_to_Table_ind_sub.sh
#PBS -S /bin/bash
#PBS -q batch
#PBS -N ${line}_snptable
#PBS -l nodes=1:ppn=10
#PBS -l mem=18gb
#PBS -l walltime=96:00:00
#PBS -m ae
#PBS -j oe

/lustre1/jcfuller/Stickleback_Genomes_Project/src/select_SNPs_to_Table.sh -s ${line} -d ${dir} -p ${pop}
EOF
)

sleep 1s
qsub /home/jcfuller/sub_scripts/select_SNPs_to_Table_ind_sub.sh
sleep 1s

done < ${sample}
