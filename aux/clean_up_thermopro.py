# CLEAN_UP_THERMPRO.PY
#  Run locally before downsampling, although we aren't sure the cleanup technique is universal!!
#  * Gets rid of non-ascii characters
#  * Concatenates date and time fields
# 
#  * TODO - get rid of any lines with a temp or rh of -.  These really mess up the plotting.
# * TODO - Integrate this with the main plotting.
#  Sometimes we  also need to fix 12 vs 24 hr clock, but that takes judgment (although it's spottable that venues are colder at night...)


# EDIT THESE VARIABLES BEFORE RUNNING

csv_filepath = "../venue-86/tranche2/raw"
csv_outpath = "../venue-86/tranche2/clean"
number_of_header_lines = 2


import pandas as pd
import os as os


csv_files = [f for f in os.listdir(csv_filepath) if os.path.isfile(os.path.join(csv_filepath, f))]
print(csv_files)

for f in csv_files:
    df = pd.read_csv(os.path.join(csv_filepath, f),encoding='utf-8-sig', usecols=[0,1,2,3], header=number_of_header_lines, names=[ 'date', 'time','temperature','rh'],dtype=str)
    df['date'] = df['date'].apply(lambda x: ''.join(char for char in x if ord(char) < 128))
    df['time'] = df['time'].apply(lambda x: ''.join(char for char in x if ord(char) < 128))
    df['time'] = df['date'] + ' ' + df['time']
    df['time'] = df['time'].apply(lambda x: x.replace('/','-')) # seems that now Thermopros output eg 15/12/2024 and we need to either read that or transform here to 15-12-2024
    df = df.drop('date',axis=1)
    mask = df['temperature'] == '-'
    # select all rows except the ones masked out
    df = df[~mask]
    #df = df.replace('-','')
    df = df.dropna()
    df.to_csv(os.path.join(csv_outpath, f),index=False)
    

