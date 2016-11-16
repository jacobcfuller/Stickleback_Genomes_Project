#!/bin/bash

echo "Give the full path of the .txt file with samples you want to run:"

read fetch

while read -r line
do

$(cat << EOF > /home/mwlab/jcfuller/stick_alignment_individual_sub.sh


/home/mwlab/jcfuller/alignment.sh -s ${line}
EOF
)

sleep 1s
qsub -q rcc-30d /home/mwlab/jcfuller/stick_alignment_individual_sub.sh
sleep 1s

done < ${fetch}
