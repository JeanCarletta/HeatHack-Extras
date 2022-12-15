# If sites run two internet-enabled monitors in the same venue, the interval between readings forms a 
# bimodal distribution with top outliers - divide by specifying bin boundaries, discarding the outliers.

# python split-by-sensor-unit.py venue_10_with_device_58BF25DB81A1.csv 2.5 4.5
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Split a csv file resulting from running two internet-enabled monitors in the same venue into separate sensor files.')
parser.add_argument('infile',  type=str, help="csv input filename")
parser.add_argument('bin_boundary_value',  type=float, help="value that separates the two bins, in minutes")
parser.add_argument('outlier_bound',  type=float, help="value above which reading interval is an outlier, not just in the upper bin") 
args = parser.parse_args()

df = pd.read_csv(args.infile)
df["timestamp"] = pd.to_datetime(df['timestamp'])
df = df.drop('voltage', axis=1) # often NaN, just get rid of it
df = df.dropna(axis=0, how="any") 


# delta is elapsed time between df['timestamp'].iloc[x-1] and x 
df['delta'] = df['timestamp'].diff(periods=1) /np.timedelta64(1, 'm')
#outliers = df[df['delta'] >= args.outlier_bound]
#df = df[df['delta'] < args.outlier_bound]

# assign a trace based on the elapsed time since the preceding data point.

df.loc[df['delta'] > args.outlier_bound, 'assignment'] = 'switch'
df.loc[(df['delta'] <= args.outlier_bound) & (df['delta'] >args.bin_boundary_value), 'assignment'] = 'sensor2'
df.loc[(df['delta'] <= args.bin_boundary_value), 'assignment'] = 'sensor1'

sensor1_df = df[df['assignment']=='sensor1']
sensor2_df = df[df['assignment']=='sensor2']
sensor1_df = df.drop(['delta','assignment'], axis=1)
sensor2_df = df.drop(['delta','assignment'], axis=1)

sensor1_df.to_csv("venue_10_sensor_1.csv", encoding='utf-8')
sensor2_df.to_csv("venue_10_sensor_2.csv", encoding='utf-8')