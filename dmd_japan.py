import json
import numpy as np
import matplotlib.pyplot as plt
import pydmd as dmd

plt.close("all")

with open('GeonetTimeSeries.json') as json_file:  
    data = json.load(json_file)

station_idx = 1
station_data = data[station_idx]
print(station_data.keys())

# Loop over all time series and extract starts and stops
for i in range(0, 10):
    station_current = data[i]
    print(len(station_current["lon"]))
    print(station_current["start"])

# Try dynamic mode decomposition
input_data_1 = np.array(station_data["lon"][1000:3000]).T
input_data_2 = np.array(station_data["lat"][1000:3000]).T
input_data = np.vstack((input_data_1, input_data_2))
dmdout = dmd.DMD(svd_rank=1, tlsq_rank=2, exact=True, opt=True)
dmdout.fit(input_data)


# Plot decomposition
plt.figure()
plt.plot(input_data_2, "r.")
plt.plot(dmdout.reconstructed_data[1, :], "-k", linewidth=0.5)
# plt.plot(dmdout.dynamics[1, :], "-b", linewidth=0.5)

plt.show(block=False)



