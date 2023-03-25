# CORRECT-TIME.PY
# When running without internet, our Pi doesn't know the correct time.  When it is on, it just counts 
# forward from the last time it was connected to the internet.  We have the user record the time
# they start and stop the Pi and send them to us.  We then need to adjust the times using an offset.
# In Excel this can be done by entering the correct time in a cell, finding the difference between
# that time and the first time in the file (straight subtraction even though it is date formats), 
# and creating a new column that adds that difference to every timestamp.  We can expect some drift
# from the clock speed, but if it's far out then the pi has been power-cycled; the error logs will
# give an indication of when.  We haven't bothered correcting for drift so far but if it is substantive,
# the same techniques we use for the standalone temperature monitors would work.
#
# This script only handles the simple case of no power-cycling and tolerable drift. 
#
#     
#
# USAGE:   python correct-time.py INFILENAME OUTFILENAME TRUE_START_DATE_TIME
# EXAMPLE: python correct-time.py currentcost_20230305212535.csv output.csv "2023-03-09 11:51"
# 
# INPUT CSV FIELDS: timestamp, field1, field2, field3 (file has no header)
# OUTPUT CSV FIELDS: corrected_datetime,field1,field2,field3 (file includes header)

import numpy as np
import pandas as pd
from datetime import datetime 


import sys

if (len(sys.argv) != 4):
    print("Usage: py correct-time.py INFILENAME OUTFILENAME TRUE_START_DATE_TIME") 
    exit(0)

infile = sys.argv[1]
outfile = sys.argv[2]
start = sys.argv[3]
    

header = "recorded_time,field1,field2,field3,corrected_datetime"

df = pd.read_csv(sys.argv[1],names=["pi_time","field1","field2","field3"])
df['recorded_time'] = df.apply(lambda row: datetime.strptime(row.pi_time,'%Y-%m-%d %H:%M:%S'), axis=1)
first_time_in_file = df.recorded_time[0]

actual_start_time = datetime.strptime(start, '%Y-%m-%d %H:%M')
offset = actual_start_time - first_time_in_file
print(first_time_in_file, actual_start_time, offset)

df['timestamp'] = df['recorded_time'] + offset 
print(df.iloc[-1])

df.to_csv(outfile, index=False, columns=["timestamp","field1","field2","field3"])
