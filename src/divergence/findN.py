#!/home/jcfuller/anaconda3/bin/python3.5

import numpy as np

fa_file = ("/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project/doc"
           "/Y_Chr_JoinedAssembly.fa")

N_count_list = []
pos = 0
N_count = 0
with open(fa_file) as fa:
    header = next(fa)
    for line in fa:
        for base in line:
            pos += 1
            if base is 'N':
                N_count += 1
            if (pos % 1000) == 0:
                if N_count >= 500:
                    N_count_list.append(0)
                else:
                    N_count_list.append(float('nan'))
                N_count = 0

np.savetxt("Y_N_count.txt", np.asarray(N_count_list))
