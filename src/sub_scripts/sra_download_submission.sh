#!/bin/bash

# Retrieve sample from arg
while getopts ":a:p:d:" opt; do
  case $opt in
    a)
      export fetch=$OPTARG
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

$(cat << EOF > /home/jcfuller/sub_scripts/sra_download_submision_ind.sh
#PBS -S /bin/bash
#PBS -q batch
#PBS -N ${line}_download
#PBS -l nodes=1:ppn=1:AMD
#PBS -l mem=1gb
#PBS -l walltime=96:00:00
#PBS -m ae
#PBS -j oe

/home/jcfuller/scripts/download_sra_and_convert_to_fastq.sh -a ${line} -d ${dir} -p ${pop}
EOF
)

sleep 1s
qsub /home/jcfuller/sub_scripts/sra_download_submision_ind.sh
sleep 1s

done < ${fetch}
