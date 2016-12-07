#!/home/jcfuller/anaconda3/bin/python3.5

import pandas as pd
import numpy as np

POM544_POF543 = "/home/jcfuller/Documents/White_lab/Stickleback_Genomes_Project\
/data/depth_analysis/Pacific_Ocean/unmasked/POM544_POF543_unmasked.txt"

df = pd.read_csv(POM544_POF543)
bp = np.arange(len(df))

# create true bp position, not just index count
bp = bp * 250
bp = bp + 2200000

logDF = pd.DataFrame(index=bp)

# create new DF with log values and accurate bp pos index
logDF['log'] = df['log(male/female)'].values
