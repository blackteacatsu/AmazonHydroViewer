import regionmask
import geopandas as gpd
import xarray as xr


def get_zonal_average_or_maximum(geodataframe_path: str, gridded_ds: xr.Dataset, pfaf_id: int, variable: str, lon:xr.DataArray, lat:xr.DataArray):

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
        print(f"An unexpected error occurred: {e}")


