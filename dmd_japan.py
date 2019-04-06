import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pydmd as dmd

plt.close("all")


with open('GeonetTimeSeries.json') as json_file:  
    data = json.load(json_file)

n_stations = len(data)
station_idx = 1
station_data = data[station_idx]

# Loop over all time series and extract starts and stops
all_start_seconds = np.zeros(n_stations)
all_n_days = np.zeros(n_stations)
for i in range(0, len(data)):
    station_current = data[i]
    all_start_seconds[i] = station_current["start"]
    all_n_days[i] = len(station_current["lon"])

all_start_days = np.round((all_start_seconds - all_start_seconds.min()) / 86400).astype(int)
all_end_days = (all_start_days + all_n_days).astype(int)

lon_mat = np.zeros((n_stations, all_end_days.max().astype(int)))
lat_mat = np.zeros((n_stations, all_end_days.max().astype(int)))


for i in range(0, len(data)):
    lon_mat[i, all_start_days[i] : all_end_days[i]] = data[i]["lon"]
    lat_mat[i, all_start_days[i] : all_end_days[i]] = data[i]["lat"]

# Subtract out mean of each time series?
# FIll in missing data with linear interpolation?
# lon_mat[lon_mat == 0] = np.nan
# lat_mat[lat_mat == 0] = np.nan

plt.matshow(lon_mat[600:800, 3000:4000])
# plt.matshow(lat_mat[600:800, 3000:4000])



# Do I have to find a maximium sized submatrix with no nans?
# https://www.geeksforgeeks.org/maximum-size-sub-matrix-with-all-1s-in-a-binary-matrix/

# # Try dynamic mode decomposition
# dmdout = dmd.DMD(svd_rank=10, tlsq_rank=10, exact=True, opt=True)
dmdout = dmd.DMD(svd_rank=1)
dmdout.fit(lon_mat[600:800, 3000:4000])


# Plot decomposition
plt.matshow(dmdout.reconstructed_data.real)
plt.show(block=False)
