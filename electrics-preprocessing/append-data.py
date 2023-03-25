# APPEND-DATA.PY
# Take two output files from correct-time.py for different data runs
# and append the data to create one file.
# we can't just use cat because of the header row in the second file.
#
# USAGE:   python correct-time.py FIRSTINFILE SECONDINFILE OUTFILE

import numpy as np
import pandas as pd
from datetime import datetime 


import sys

if (len(sys.argv) != 4):
    print("Usage: py correct-time.py INFILEONE INFILETWO OUTFILENAME") 
    exit(0)

infile = sys.argv[1]
infiletwo = sys.argv[2]
outfile = sys.argv[3]

    

df1 = pd.read_csv(infile)
print(df1)

df2 = pd.read_csv(infiletwo)
print(df2)

df3 = pd.concat([df1,df2])
print(df3)

df3.to_csv(outfile, index=False, columns=["timestamp","field1","field2","field3"])
