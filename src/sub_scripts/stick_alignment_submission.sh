#!/bin/bash

# Retrieve sample from arg
while getopts ":s:" opt; do
  case $opt in
    s)
      export fetch=$OPTARG
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


$(cat << EOF > /home/jcfuller/stick_alignment_individual_sub.sh

#PBS -S /bin/bash
#PBS -q batch
#PBS -N ${line}
#PBS -l nodes=1:ppn=8
#PBS -l mem=16gb
#PBS -l walltime=96:00:00
#PBS -m ae
#PBS -j oe


/lustre1/jcfuller/Stickleback_Genomes_Project/src/alignment_masked.sh -s ${line}
EOF
)

sleep 1s
qsub /home/jcfuller/stick_alignment_individual_sub.sh
sleep 1s

done < ${fetch}
