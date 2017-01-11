#!/bin/bash

# Retrieve sample from arg
while getopts ":s:p:" opt; do
  case $opt in
    s)
      export fetch=$OPTARG
      ;;
    p)
      export pop=${OPTARG}
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


$(cat << EOF > /home/jcfuller/sub_scripts/stick_alignment_individual_sub.sh

#PBS -S /bin/bash
#PBS -q batch
#PBS -N ${line}
#PBS -l nodes=1:ppn=8:AMD
#PBS -l mem=16gb
#PBS -l walltime=96:00:00
#PBS -m ae
#PBS -j oe


/home/jcfuller/scripts/alignment_Y.sh -s ${line} -p ${pop}
EOF
)

sleep 1s
qsub /home/jcfuller/sub_scripts/stick_alignment_individual_sub.sh
sleep 1s

done < ${fetch}
