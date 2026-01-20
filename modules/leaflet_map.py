"""
ipyleaflet integration for Shiny app
Replaces Plotly heatmap with tile-based map
"""

from ipyleaflet import Map, basemaps, TileLayer, GeoJSON, WidgetControl
from ipywidgets import HTML
import requests
import json
import shared

def create_hydrobasin_map():
    """
    Create ipyleaflet map with HydroBasins overlay
    
    tile_server_url="http://localhost:5000"

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
        center=[-7, -66],
        zoom=4.5,
        scroll_wheel_zoom=True,
        basemap=basemaps.CartoDB.Voyager  # Or no basemap so we can add custom
    )

    # request polygon layer of hydrobasins lvl.5
    r = requests.get(shared.hydrobasins_lev05_url)
    geojson_data = r.json()
    
    polygon_layer = GeoJSON(
    data=geojson_data,
    style={
        'color': 'grey',
        'weight': 0.6,
        'fillOpacity': 0,
        'opacity': 1
    },
    hover_style={
        'color': 'grey',
        'weight': 0,
        'fillOpacity': 0.4
    },
    name='HydroBasins @lvl 5'
    )

    # CSS styling to match app font
    hover_style = """
        font-family: 'Space Grotesk', sans-serif;
        font-size: 14px;
        padding: 8px 12px;
        background: white;
        border-radius: 4px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.2);
    """
    hover_info = HTML(value=f'<div style="{hover_style}"><b>Hover over a basin</b></div>')
    hover_control = WidgetControl(widget=hover_info, position='topright')
    m.add_control(hover_control)

    def on_hover(event, feature, **kwargs):
        pfaf_id = feature['properties'].get('PFAF_ID', 'N/A')
        hover_info.value = f'<div style="{hover_style}"><b>Regional PFAF ID:</b> {pfaf_id}</div>'
    
    polygon_layer.on_hover(on_hover)

    m.add_layer(polygon_layer)

    # Placeholder for data tiles (will be updated reactively)
    # data_layer = None

    return m, polygon_layer

# def update_data_layer(
#         map_widget,
#         #old_layer,
#         variable,
#         time_idx,
#         category,
#         profile=0,
#         colormap='Reds',
#         tile_server_url="http://localhost:5000"
# ):
#     # Remove old layer if not None:
#     # if old_layer is not None:
#     #     map_widget.remove(old_layer)
    
#     # Build tile URL
#     requests.get(f"{tile_server_url}/cache/clear")
#     print("✓ Cache cleared")
#     tile_url = f"{tile_server_url}/tiles/{variable}/{time_idx}/{category}/{{z}}/{{x}}/{{y}}.png"

#     "?colormap={colormap}&profile={profile}&mode=global&tms=true&vmin={vmin}&vmax={vmax}"
#     #Add query parameters
#     params = []
#     if colormap:
#         params.append(f"colormap={colormap}")
#         params.append(f"profile={profile}&mode=global&tms=true")
    
#     if params:
#         tile_url += "?" + "&".join(params)
#     # print(tile_url)
#     # Create new layer
#     forecast_layer = TileLayer(
#         url=tile_url,
#         name=shared.list_of_variables.get(variable),
#         opacity=1,
#         attribution='HydroViewer',
#         min_native_zoom = 4,
#         max_native_zoom = 9
#     )
    
#     # Add to map
#     return forecast_layer

# # Handle click event on the polygon layer
def polygon_click_handler(polygon_layer, callback):
    def on_click(feature, **kwargs):
        if feature and 'properties' in feature:
            pfaf_id = feature['properties'].get('PFAF_ID', 'N/A')
            if pfaf_id:
                callback(pfaf_id)

    polygon_layer.on_click(on_click)

# hover_info = HTML(value='<b>Hover over a basin</b>')
# def polygon_hover_handler(polygon_layer, callback):
#     def on_hover(feature, **kwargs): # Define hover callback to show pfaf_id
#         pfaf_id = feature['properties'].get('PFAF_ID', 'N/A')
#         hover_info.value = f'<b>Regional PFAF ID:</b> {pfaf_id}'
    
#     polygon_layer.on_hover(on_hover)