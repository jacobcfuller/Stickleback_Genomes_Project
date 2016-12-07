#!/bin/bash

# Retrieve sample from arg
while getopts ":s:d:" opt; do
  case $opt in
    s)
      export fetch=$OPTARG
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

while read -r line
do

$(cat << EOF > /home/jcfuller/sub_scripts/bedtools_sub_inside.sh
#PBS -S /bin/bash
#PBS -q batch
#PBS -N ${line}_depth
#PBS -l nodes=1:ppn=3
#PBS -l mem=6gb
#PBS -l walltime=96:00:00
#PBS -m ae
#PBS -j oe

/lustre1/jcfuller/Stickleback_Genomes_Project/src/bedtools_depth_txt.sh -s ${line} -d ${dir}
EOF
)

sleep 1s
qsub /home/jcfuller/sub_scripts/bedtools_sub_inside.sh
sleep 1s

done < ${fetch}
