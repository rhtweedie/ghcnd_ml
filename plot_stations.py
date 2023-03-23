from mpl_toolkits.basemap import Basemap
from PIL import Image as im
import matplotlib.pyplot as plt
import numpy as np
import json
from GHCND import *

# create instance of the GHCND class and extract information on countries and stations from their respective files
ghn = GHCND()
ghn.readCountriesFile()
ghn.readStationsFile()

# get list of station names
station_names = ghn.getStatKeyNames()

lons = []
lats = []

for i in range(len(ghn.stationDict)):
    lons.append(ghn.stationDict[station_names[i]].lon)
    lats.append(ghn.stationDict[station_names[i]].lat)

# create new figure, axes instances.
fig = plt.figure(figsize=(10, 10))
ax = fig.add_axes([0.5, 0.5, 0.5, 0.5])
# setup mercator map projection.
map = Basemap(llcrnrlon=-180., llcrnrlat=-80., urcrnrlon=180., urcrnrlat=80.,
              rsphere=(6378137.00, 6356752.3142),
              resolution='l', projection='merc',
              lat_0=40., lon_0=-20., lat_ts=20.)
map.drawcoastlines()
map.fillcontinents()
map.drawparallels(np.arange(-90, 90, 20), labels=[1, 1, 0, 1])
map.drawmeridians(np.arange(-180, 180, 30), labels=[1, 1, 0, 1])
ax.set_title('GCN Stations')

for i in range(len(lats)):
    x, y = map(lons[i], lats[i])
    map.plot(x, y, 'ro', markersize=1.5)

file_name = 'report/all_stations.png'
plt.savefig(file_name, format='png')
print(f"Image saved at {file_name}")
