# How to preprocess electric data before hosting on web

The raw data is very frequent, 6s intervals.

- If the logger ran in "save to SD card" mode, use **correct-time.py** with the hand-recorded start time to adjust the timings.  
Check the last recorded time in the data file against the hand-recorded end time to see how bad the drift is and inform the venue.  
Then store the full data privately for them (currently Google Drive). 

:TODO: add drift correction to the processing.

- downsample the data using **downsample.py**

- Create a private html with the full scale data by modifying the notebook in electrics-processing and running jupyter nbconvert --to html FILE.ipynb
can be run through jupyter-book on the laptop processing and the resulting html hosted privately. 



- if a new group, add a new notebook for the downsampled data, test the jupyter book build with jupyter-book build . --builder html, commit and push to host be careful to omit anything unwanted.
We have a safety timeout on Github processing to be sure we don't incur charges or waste resource, so we don't push the full data and certainly don't push a notebook that builds using it.

- otherwise append the downsampled data to the previous data file (filed under venue) using **append-data.py**.

