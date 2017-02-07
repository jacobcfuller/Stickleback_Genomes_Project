#!/bin/bash

# Retrieve sample from arg
while getopts ":a:i:d:" opt; do
  case $opt in
    a)
      export line=$OPTARG
      ;;
    d)
      export dir=$OPTARG
      ;;
    i)
      export ind=$OPTARG
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

$(cat << EOF > /home/jcfuller/sub_scripts/sra_download_submision_ind.sh
#PBS -S /bin/bash
#PBS -q batch
#PBS -l nodes=1:ppn=1:AMD
#PBS -l mem=1gb
#PBS -l walltime=96:00:00
#PBS -m ae
#PBS -j oe

/home/jcfuller/scripts/download_sra_and_convert_to_fastq.sh -a ${line} -d ${dir} -i ${ind}
EOF
)

sleep 1s
qsub /home/jcfuller/sub_scripts/sra_download_submision_ind.sh
sleep 1s
