#!/bin/bash

echo "Give the full path of the .txt file with samples you want to run:"

read fetch

while read -r line
do

$(cat << EOF > /home/jcfuller/scripts/stick_alignment_individual_sub.sh
#PBS -S /bin/bash
#PBS -q batch
#PBS -N ${line}
#PBS -l nodes=1:ppn=12:AMD
#PBS -l mem=2gb
#PBS -l walltime=96:00:00
#PBS -M jacobcfuller93@gmail.com
#PBS -m ae
#PBS -j oe

/home/jcfuller/scripts/alignment.sh -s ${line}
EOF
)

sleep 1s
qsub /home/jcfuller/scripts/stick_alignment_individual_sub.sh
sleep 1s

done < ${fetch}
