#DOWNSAMPLE-DATA.PY
# CurrentCost monitors produce too much data to stick in a Jupyter book - a week is OK,
# but more than that and the execution times really climb.  Downsample the data to half-hourly
# averages over the three phases combined, assuming simple arithmetic addition for the combination
# (which we think is appropriate for the way three phases are used in these buildings)
# and also write daily kWh summaries.  


# USAGE:   python downsample-data.py INFILENAME OUTFILENAME_DOWNSAMPLED_DATA OUTFILENAME_DAY_TOTALS
# EXAMPLE: python downsample-data.py currentcost_20230305212535.csv venue_20_electricity_downsampled.csv venue_20_elecricity_by_day.csv

import numpy as np
import pandas as pd

import sys

if (len(sys.argv) != 4):
    print("Usage: python downsample-data.py INFILENAME OUTFILENAME_DOWNSAMPLED_DATA OUTFILENAME_DAY_TOTALS") 
    exit(0)

infile = sys.argv[1]
outfile_downsampled = sys.argv[2]
outfile_day = sys.argv[3]

df = pd.read_csv(infile)
df["timestamp"] = pd.to_datetime(df['timestamp'])
df["total_kW"] = (df['field3']+df['field2']+df['field1'])/1000
df = df.fillna(value=0)

# downsample to 30 minute intervals

df.field1 = df.field1.astype(int)
df.field2 = df.field2.astype(int) 
df.field3 = df.field3.astype(int)

# aggregate over 30 minute intervals - this is the interval for smart meter readings.
s = df.resample('30T', on='timestamp', origin='start').agg({'field1':'mean','field2':'mean','field3':'mean'})
s = s.fillna(value=0)
s['total_kW'] = (s['field1'] + s['field2'] + s['field3'])/1000

s.to_csv(outfile_downsampled, encoding='utf-8')

# downsample to one day intervals, for summary stats

d = df.resample('1D', on='timestamp', origin='start_day').agg({'total_kW':'mean'})
d['kwh'] = d['total_kW']*24
d= d.fillna(value=0)

d.to_csv(outfile_day, encoding='utf-8')

# save a one week extract of the full data

#one_week_df = df[(df['timestamp'] > pd.to_datetime('2023-02-16 00:00:00')) & (df['timestamp'] < pd.to_datetime('2023-02-22 00:00:00'))]
#print(one_week_df.iloc[0])
#print(one_week_df.iloc[-1])

#one_week_df.to_csv("venue_20_electricity_one_week_detail.csv", encoding='utf-8')


