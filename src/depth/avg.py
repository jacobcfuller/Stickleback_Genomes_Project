#!/home/jcfuller/anaconda3/bin/python3.5

import depth
import pandas as pd
'''just a script to save some output from depth.py to .csv
'''
popAvgDict = depth.avg_pops()

avg_DF = pd.concat(popAvgDict, axis=1)

avg_DF.to_csv("pops_avg_reads.csv")
