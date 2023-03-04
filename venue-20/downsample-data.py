# Too much data from CurrentCosts - get a one week extract, and downsample the whole thing.

import numpy as np
import pandas as pd

df = pd.read_csv("venue-20-clampon-data.csv")
df["timestamp"] = pd.to_datetime(df['corrected_datetime'])
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

s.to_csv("venue_20_electricity_downsampled.csv", encoding='utf-8')

# downsample to one day intervals, for summary stats

d = df.resample('1D', on='timestamp', origin='start_day').agg({'total_kW':'mean'})
d['kwh'] = d['total_kW']*24
d= d.fillna(value=0)

d.to_csv("venue_20_electricity_by_day.csv", encoding='utf-8')

# save a one week extract of the full data

one_week_df = df[(df['timestamp'] > pd.to_datetime('2023-02-16 00:00:00')) & (df['timestamp'] < pd.to_datetime('2023-02-22 00:00:00'))]
#print(one_week_df.iloc[0])
#print(one_week_df.iloc[-1])

one_week_df.to_csv("venue_20_electricity_one_week_detail.csv", encoding='utf-8')


