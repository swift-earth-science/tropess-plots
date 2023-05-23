import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
from scipy.interpolate import griddata
from scipy.spatial import cKDTree


def plot_x_col_mesh_ckdtree(max_distance_degrees=5):
    # Open the netCDF file
    dataset = Dataset('data/TROPESS_CrIS-JPSS1_L2_Summary_CH4_20230516_MUSES_R1p20_FS_F0p6.nc', 'r')

    # Read the data from your variables
    latitude = dataset.variables['latitude'][:]
    longitude = dataset.variables['longitude'][:]
    x_col_p = dataset.variables['x_col_p'][:]

    dataset.close()

    # Specify figure size (in inches)
    dpi=300; w=3600 / dpi; h=2400 / dpi
    plt.figure(figsize=(w, h))  

    # Create a basemap instance
    m = Basemap(projection='cyl', resolution='l',
                llcrnrlat=-90, urcrnrlat=90,  # set latitude limits to -90 and 90
                llcrnrlon=-180, urcrnrlon=180)  # set longitude limits to -180 and 180

    m.drawcoastlines(linewidth=0.5)
    m.drawcountries(linewidth=0.5)

    # Draw parallels (latitude lines) and meridians (longitude lines)
    parallels = np.arange(-90., 91., 30.)
    m.drawparallels(parallels, labels=[True,False,False,False], linewidth=0.3)

    meridians = np.arange(-180., 181., 60.)
    m.drawmeridians(meridians, labels=[False,False,False,True], linewidth=0.3)

    # Get the grid for the interpolated values
    grid_lat, grid_lon = np.mgrid[-90:91:1, -180:181:1]

    # Interpolate the data using griddata
    grid_x_col_p = griddata((latitude, longitude), x_col_p, (grid_lat, grid_lon), method='linear')

    # Find the distance to the nearest original point for each point in the interpolated grid
    tree = cKDTree(np.vstack((latitude, longitude)).T)
    dist, _ = tree.query(np.vstack((grid_lat.ravel(), grid_lon.ravel())).T)

    # Reshape the distance array to have the same shape as the x_col_p grid
    dist_grid = dist.reshape(grid_x_col_p.shape)

    # Mask the interpolated values that are too far from any original point
    grid_x_col_p[dist_grid > max_distance_degrees] = np.nan

    # Plot the interpolated data using pcolormesh instead of scatter
    sc = m.pcolormesh(grid_lon, grid_lat, grid_x_col_p, latlon=True, cmap='jet')

    # Add a colorbar
    cbar = m.colorbar(sc, location='bottom', pad="10%")
    cbar.set_label('x_col_p')

    # Save figure to PNG file
    plt.savefig(f'plots/figure_ckdtree_{max_distance_degrees}_degrees.png', dpi=dpi, bbox_inches='tight')