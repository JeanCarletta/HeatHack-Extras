# CORRECT-TIME.PY
# Messed around copy of electrics processing to work for a one-off standalone monitor file
# with similar timing problems.

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
# IMPORTANT:  the provided true start date-times will be in local time, but must be expressed
# on the command line as UTC.
#
# :TODO: handle drift correction?? Not important so far.
# :TODO: ensure handling is correct for time zone.  
## 
## :BUG: notebook shows a 2 hour gap at the time change, not sure why
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
    print("Usage: py correct-time.py INFILENAME OUTFILENAME TRUE_START_DATE_TIME where the date time is UTC, not BST") 
    exit(0)

infile = sys.argv[1]
outfile = sys.argv[2]
start = sys.argv[3]


header = "recorded_time,temperature,rh"

df = pd.read_csv(sys.argv[1]) #names=["pi_time","temperature","rh"])
print(df)

# code for finding stray pi_times that don't read as strings.  We got NaNs from bad characters at 
#end of file; if this persists just remove any lines that contain non-strings in the pi_time field!
# types = df.pi_time.apply(type).unique()
# for element in types:
#     print(element)

## get rid of NaNs.
#df = df.dropna()

df['recorded_time'] = df.apply(lambda row: datetime.strptime(row.pi_time,'%Y-%m-%dT%H:%M:%SZ'), axis=1)
first_time_in_file = df.recorded_time[0]

actual_start_time = datetime.strptime(start, '%Y-%m-%d %H:%M')

offset = actual_start_time - first_time_in_file
print(first_time_in_file, actual_start_time, offset)
print(df['recorded_time'].iloc[-1])
print(type(df['recorded_time'].iloc[-1]))

df['timestamp'] = df['recorded_time'] + offset 

# :TODO: add a T and Z here to make it explicit.
print(df['timestamp'].iloc[-1])
print(type(df['timestamp'].iloc[-1]))

### add non_existent="shift_forward"??  filter NaT?
df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('UTC') 


print(df['timestamp'].iloc[-1])
print(type(df['timestamp'].iloc[-1]))

df.to_csv(outfile, index=False, columns=["timestamp","temp","rh"], header=False, date_format = "%Y-%m-%dT%H:%MZ")
