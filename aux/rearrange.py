import os as os
import pandas as pd
 
csv_filepath = "../venue-87/thermopro1"
csv_outpath = "../venue-87/rearranged"
number_of_header_lines = 1

csv_files = [f for f in os.listdir(csv_filepath) if os.path.isfile(os.path.join(csv_filepath, f))]
print(csv_files)


for f in csv_files:
    df = pd.read_csv(os.path.join(csv_filepath, f),encoding='utf-8-sig', usecols=[0,1,2,3], header=number_of_header_lines, names=[ 'baddatetime','temperature','rh','time'],dtype=str)
    df = df.drop('baddatetime',axis=1)

    df.to_csv(os.path.join(csv_outpath, f),columns=['time','temperature','rh'],index=False)