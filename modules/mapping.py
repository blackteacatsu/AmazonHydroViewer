import json
import urllib.request
import plotly.graph_objects as go
import xarray as xr
import pooch
from shared import probabilistic_data_path
from modules import plotly_theme
#import os

# Read gridded data files and find coordinates variable
def get_standard_coordinates(dataset: xr.Dataset, lon_names=None, lat_names=None, time_names=None):
    """
    Retrieve longitude, latitude, and time variables from an xarray dataset,
    accommodating different naming conventions.

    Parameters:
        dataset (xr.Dataset): The xarray dataset to search.
        lon_names (list): List of possible names for longitude (default: common names).
        lat_names (list): List of possible names for latitude (default: common names).
        time_names (list): List of possible names for time (default: common names).

    Returns:
        tuple: Longitude, latitude, and time variables.

    Raises:
        AttributeError: If any of the required variables are not found.
    """

    lon_names = lon_names or ["east_west", "lon", "longitude"]
    lat_names = lat_names or ["north_south", "lat", "latitude"]
    time_names = time_names or ["time"]

    def find_variable(dataset, possible_names):
        for name in possible_names:
            if name in dataset.variables:
                return dataset[name]
        raise AttributeError(f"None of the variable names {possible_names} found in the dataset.")

    # Try to find longitude, latitude, and time variables
    lon = find_variable(dataset, lon_names)
    lat = find_variable(dataset, lat_names)
    time = find_variable(dataset, time_names)

    return lon, lat, time

# This function retrieves data from a remote URL and returns the dataset along with its standard coordinates.
def retrieve_data_from_remote(var, profile):

    """if data_type == "Probabilistic":
    url = probabilistic_data_path + var + "_lvl_" + profile + ".nc"
        # Check if the URL is valid and accessible
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError(f"Invalid URL: {url}. Ensure it starts with 'http://' or 'https://'.")
    """
    if var not in ["SoilTemp_inst", "SoilMoist_inst"]: 
        profile = "0"
    url = probabilistic_data_path + var + "_lvl_" + profile + ".nc"
    # Check if the URL is valid and accessible

    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError(f"Invalid URL: {url}. Ensure it starts with 'http://' or 'https://'.")
    
    # Use pooch to download the file and open it as an xarray dataset
    #temp_file = tempfile.NamedTemporaryFile(delete=False).name  # Create a temporary file to store the downloaded data
    temp_file = pooch.retrieve(url, known_hash=None)
    
    with xr.open_dataset(temp_file, engine='netcdf4') as ds_forecast:
        ds_forecast.load() # Load the dataset into memory
        lon, lat, time = get_standard_coordinates(ds_forecast) # Retrieve standard coordinates
    
    #os.remove(temp_file)  # Clean up the temporary file after loading
    return ds_forecast, lon, lat, time

# Building polygon maps using geojson 
def buildregion(path_to_geojson):
    with urllib.request.urlopen(path_to_geojson) as url:
        geojson = json.loads(url.read().decode()) 
    
    # Combine all polygons into one trace
    polygon_x = []  # Store all x-coordinates
    polygon_y = []  # Store all y-coordinates
    polygon_text = []  # Store hover text (PFAF_ID)
    
    for feature in geojson['features']:
        pfaf_id = feature['properties']['PFAF_ID']
        if feature['geometry']['type'] == 'Polygon':
            x, y = zip(*feature['geometry']['coordinates'][0])
            polygon_x.extend(x + (None,))  # Add None to break the line between polygons
            polygon_y.extend(y + (None,))
            polygon_text.extend([pfaf_id] * len(x) + [None])  # Add None for breaks
        elif feature['geometry']['type'] == 'MultiPolygon':
            for polygon in feature['geometry']['coordinates']:
                x, y = zip(*polygon[0])
                polygon_x.extend(x + (None,))
                polygon_y.extend(y + (None,))
                polygon_text.extend([pfaf_id] * len(x) + [None])


    # Add a single trace for all polygons
    heatmap=go.FigureWidget(
        go.Scatter(
        x=polygon_x,
        y=polygon_y,
        mode='lines',
        line=dict(color='white', width=1.5),
        text=polygon_text,
        hoverinfo='text',
        hovertemplate='PFAF_ID: %{text}<extra></extra>'
        )
    )

    # Apply Brutalist theme for map visualization
    heatmap.update_layout(**plotly_theme.get_map_layout())

    return heatmap
