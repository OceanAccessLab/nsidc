'''
Script to combined MASAM2 daily data into a collated product

Run into: /home/cyrf0006/data/NSIDC/MASAM2

Frederic.Cyr@dfo-mpo.gc.ca
March 2024


'''

import os
import numpy as np
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import netCDF4


## Some parameters ##
path =  '/home/cyrf0006/data/NSIDC/MASAM2/'
latLims = [40, 70]
lonLims = [-80, -50]


# Loop on individual files
for idx, file in enumerate(sorted(os.listdir(path))):
    filename = os.path.join(path, file)
    # open file
    print('Get ' + filename)
    ds_tmp = xr.open_dataset(filename)

    ds_tmp = ds_tmp.mean('t')

    # find dates
    YYYY = filename.split('.')[1][0:4]
    MM = filename.split('.')[1][4:6]
    DD = str(15)
    datetime = pd.to_datetime(YYYY+'-'+MM+'-'+DD)
    
    # Replace time dimension
    # (https://groups.google.com/g/xarray/c/QeI66hHcU1k/m/nlTzefzZCwAJ)
    ds_tmp['datetime'] = datetime
    ds_tmp = ds_tmp.drop('Day_of_Month')
    
    # Open, concat & save
    if idx == 0:
        ds = ds_tmp.copy()
        ds.to_netcdf('masam2_combined.nc')
        ds.close()
    else:
        ds = xr.open_dataset('masam2_combined.nc')
        ds = xr.concat([ds, ds_tmp], dim='time')
        ds.to_netcdf('masam2_combined.nc')        
        ds.close()
        
    ds_tmp.close()


    
