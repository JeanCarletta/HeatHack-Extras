# DOWNSAMPLE.PY
#  downsample the data from every 1 minute to every 5, and also get rid of everything before a given start time.
## take a safe copy of the data before proceeding - routine is destructive
## be careful that the data is suitable - the python routine used can also upsample.
## tries to convert all files in the directory, even use diaries, even non-CSVs.

# EDIT THESE VARIABLES BEFORE RUNNING

omit_before = "26-11-2024 09:00" #"2024-11-25T00:00:00Z"
csv_filepath = "../venue-86/"


import pandas as pd
import os as os
desired_start = pd.to_datetime(omit_before)


def timezoneString(hoursAhead):   
    if (hoursAhead==0): 
        return "GMT"
    elif (hoursAhead==1):
        return "BST" 
    else:
        return ("time error")



csv_files = [f for f in os.listdir(csv_filepath) if os.path.isfile(os.path.join(csv_filepath, f))]
print(csv_files)
for f in csv_files:


    dfTempDataSet = pd.read_csv(os.path.join(csv_filepath, f),encoding='latin-1',usecols=[0,1,2], header=1, names=[ 'time','temperature','rh']) 
    if (len(dfTempDataSet)>0):
        print("1: ", len(dfTempDataSet))
        dfTempDataSet = dfTempDataSet.dropna(subset=['temperature','rh'])
        print("2: ", len(dfTempDataSet))
        dfTempDataSet["timestamp"] = pd.to_datetime(dfTempDataSet['time'], dayfirst=True)
        #dfTempDataSet = dfTempDataSet[pd.to_datetime(dfTempDataSet['time']).dt.tz_convert("Europe/London") >= pd.to_datetime(omit_before)]
        dfTempDataSet = dfTempDataSet.set_index(['timestamp'])
        print("3: ", len(dfTempDataSet))
        #print(type(dfTempDataSet['timestamp'][1]))
        print(dfTempDataSet.sample(6))

        dfTempDataSet = dfTempDataSet.query('index > @desired_start')
        print("4: ", len(dfTempDataSet))
       # dfTempDataSet = dfTempDataSet['timestamp'] >= desired_start
        #print(type(desired_start))
        if (len(dfTempDataSet) > 0):
                dfTempDataSet = dfTempDataSet.resample('5min').first()
                dfTempDataSet.to_csv(f, index=False)  
        else:
            print("no data after the break date")     
    else:
        print("empty data file")
