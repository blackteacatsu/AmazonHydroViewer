"""
ipyleaflet integration for Shiny app
Replaces Plotly heatmap with tile-based map
"""

from ipyleaflet import Map, basemaps, TileLayer, GeoJSON, WidgetControl
from ipywidgets import HTML
import json
import urllib.request
import shared


def create_hydrobasin_map(tile_server_url="http://localhost:5000"):
    """
    Create ipyleaflet map with HydroBasins overlay
    
    Parameters
    ----------
    tile_server_url : str
        URL of the tile server
        
    Returns
    -------
    map : ipyleaflet.Map
        Configured map widget
    polygon_layer : ipyleaflet.GeoJSON
        Polygon layer for click handling
    data_layer : ipyleaflet.TileLayer
        Data tile layer (to be updated)
    """

    # Initialize leaflet map object
    m = Map(
        center=[-7.5, -65.5],
        zoom=5,
        scroll_wheel_zoom=True,
        basemap=basemaps.Esri.WorldImagery  # Or no basemap so we can add custom

    )

    # request polygon layer of hydrobasins lvl.5
    

    return map, polygon_layer, data_layer