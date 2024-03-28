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
for idx, file in enumerate(os.listdir(path)):
    filename = os.path.join(path, file)
    # open file
    print('Get ' + filename)
    ds_tmp = xr.open_dataset(filename)

    ## # reduce region
    ## longitude = ds.Longitude.values
    ## latitude = ds.Latitude.values
    ## # find pixel
    ## idx =  np.argmin(np.abs(longitude-lonLims[]) + np.abs(latitude-df.iloc[i]['Latitude']))
    ## idxs = np.unravel_index(idx, latitude.shape)
    ## ds = ds.isel(x = idxs[1], y = idxs[0])

    # find dates
    YYYY = filename.split('.')[1][0:4]
    MM = filename.split('.')[1][4:6]
    DD = ds_tmp.t.values+1
    datetime = pd.to_datetime(YYYY+'-'+MM) + pd.to_timedelta(DD, unit='D') - pd.Timedelta(days=1)

    # Replace time dimension
    # (https://groups.google.com/g/xarray/c/QeI66hHcU1k/m/nlTzefzZCwAJ)
    ds_renamed = ds_tmp.rename({'t': 'time'})
    ds_renamed.coords['time'] = datetime
    ds_renamed = ds_renamed.drop('Day_of_Month')
    ds_tmp.close()

    # Open, concat & save
    if idx == 0:
        ds = ds_renamed.copy()
        ds.to_netcdf('masam2_combined.nc')
        ds.close()
    else:
        ds = xr.open_dataset('masam2_combined.nc')
        ds = xr.concat([ds, ds_renamed], dim='time')
        ds.to_netcdf('masam2_combined.nc')        
        ds.close()
        
    ds_renamed.close()


    
