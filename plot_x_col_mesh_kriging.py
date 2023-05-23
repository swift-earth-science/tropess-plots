import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
from pykrige.ok import OrdinaryKriging


def plot_x_col_mesh_kriging():
    # Open the netCDF file
    dataset = Dataset('data/TROPESS_CrIS-JPSS1_L2_Summary_CH4_20230516_MUSES_R1p20_FS_F0p6.nc', 'r')

    # Read the data from your variables
    latitude = dataset.variables['latitude'][:]
    longitude = dataset.variables['longitude'][:]
    x_col_p = dataset.variables['x_col_p'][:]

    dataset.close()


    # Specify figure size (in inches)
    plt.figure(figsize=(12, 8))  

    # Create a basemap instance
    m = Basemap(projection='cyl', resolution='l',
                llcrnrlat=-90, urcrnrlat=90,  # set latitude limits to -90 and 90
                llcrnrlon=-180, urcrnrlon=180)  # set longitude limits to -180 and 180

    m.drawcoastlines(linewidth=0.1)
    m.drawcountries(linewidth=0.1)

    # Draw parallels (latitude lines) and meridians (longitude lines) with a 30-degree and 60-degree spacing respectively
    parallels = np.arange(-90., 91., 30.)
    m.drawparallels(parallels, labels=[True,False,False,False], linewidth=0.3)

    meridians = np.arange(-180., 181., 60.)
    m.drawmeridians(meridians, labels=[False,False,False,True], linewidth=0.3)

    # Transform lat and lon to map projection coordinates
    x, y = m(longitude, latitude)

    # Kriging interpolation
    grid_lon, grid_lat = np.mgrid[-180:181:360j, -90:91:180j]
    OK = OrdinaryKriging(longitude, latitude, x_col_p, variogram_model='linear', verbose=False, enable_plotting=False)
    z, ss = OK.execute('grid', grid_lon.ravel(), grid_lat.ravel())
    z = z.reshape(grid_lon.shape)

    # Plot the data using pcolormesh
    sc = m.pcolormesh(grid_lon, grid_lat, z, cmap='jet', latlon=True)

    # Add a horizontal colorbar at the bottom
    cbar = m.colorbar(sc, location='bottom', pad="10%")
    cbar.set_label('x_col_p')

    # Save figure to PNG file
    plt.savefig('plots/figure_kriging.png', dpi=300, bbox_inches='tight')