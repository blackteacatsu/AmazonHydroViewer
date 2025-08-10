import regionmask
import geopandas as gpd
import xarray as xr
import pooch
from modules.mapping import get_standard_coordinates
from shared import deterministic_data_path, probabilistic_data_path
import os

#def extract_river_network_with_attributes():
## waiting to be implemented

# This function retrieves data from a remote URL and returns the dataset along with its standard coordinates.
def retrieve_data_from_remote(data_type, var, profile):

    if data_type == "Probabilistic":
        url = probabilistic_data_path + var + "_lvl_" + profile + ".nc"
        
        # Check if the URL is valid and accessible
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError(f"Invalid URL: {url}. Ensure it starts with 'http://' or 'https://'.")
        
        # Use pooch to download the file and open it as an xarray dataset
        # For probabilistic data, we retrieve netcdf files
        temp_file = pooch.retrieve(url=url, known_hash=None)
        ds_forecast = xr.open_dataset(temp_file, engine='netcdf4')
        ds_forecast.load()

    else:
        # For probabilistic or deterministic data, we retreive netcdf files
        url = deterministic_data_path + var + "_lvl_" + profile + ".nc"
        # Check if the URL is valid and accessible
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError(f"Invalid URL: {url}. Ensure it starts with 'http://' or 'https://'.")
        
        # Use pooch to download the file and open it as an xarray dataset
        temp_file = pooch.retrieve(url=url, known_hash=None)
        ds_forecast = xr.open_dataset(temp_file, engine='netcdf4')
        ds_forecast.load()  # Load the dataset into memory
    
    lon, lat, time = get_standard_coordinates(ds_forecast)
    return ds_forecast, lon, lat, time


"""# This function calculates zonal statistics for a specified PFAF_ID from a geodataframe and a gridded dataset.
def get_zonal_statistics(geodataframe_path: str, gridded_ds: xr.Dataset, 
                         pfaf_id: int, variable: str, lon:xr.DataArray, lat:xr.DataArray):
    try:
        # Read the geodataframe
        geodataframe = gpd.read_file(geodataframe_path)

        # Filter the geodataframe for the specified PFAF_ID
        aoi = geodataframe[geodataframe.PFAF_ID == pfaf_id]
        if aoi.empty:
            raise ValueError(f"No matching PFAF_ID {pfaf_id} found in the geodataframe.")

        # Create a 3D mask
        aoi_mask = regionmask.mask_3D_geopandas(aoi, lon, lat)

        # Apply the mask to the selected variable
        if variable not in gridded_ds.variables:
            raise ValueError(f"Variable '{variable}' not found in the dataset.")
        aoi_ds = gridded_ds[variable].where(aoi_mask)

        # Calculate zonal statistics
        if variable == 'Streamflow_tavg':
            # Zonal maximum for Streamflow_tavg
            summary = aoi_ds.groupby("time").max(["lat", "lon"])
        else:
            # Zonal average for other variables
            summary = aoi_ds.groupby("time").mean(["lat", "lon"])

        # Convert to DataFrame and reset index
        aoi_ds_summary = summary.to_dataframe().reset_index()
        aoi_ds_summary['time'] = aoi_ds_summary['time'].astype(str)

        # Close the dataset
        return aoi_ds_summary

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")"""


