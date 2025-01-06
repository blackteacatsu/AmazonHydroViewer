from shiny import App, ui, reactive, render
from shinywidgets import output_widget, render_plotly
import plotly.graph_objects as go
import xarray as xr
import pandas as pd
import regionmask
import numpy as np
import json
import urllib.request
import geopandas as gpd

# Load the datasets
ensemble_avg_dataset_location = '/Users/kris/amazonforcast/data/forecast/output/LIS_HIST_Forecast_June_02_to_05_mean.nc'
ensemble_members_dataset_location = '/Users/kris/amazonforcast/data/forecast/output/LIS_HIST_Forecast_June_02_to_05.nc'

ensemble_avg_dataset = xr.open_dataset(ensemble_avg_dataset_location)
ensemble_members_dataset = xr.open_dataset(ensemble_members_dataset_location)

longitude = ensemble_avg_dataset['east_west']
latitude = ensemble_avg_dataset['north_south']
time = ensemble_avg_dataset['time']

# Load the GeoJSON file
geojson_url = "https://raw.githubusercontent.com/blackteacatsu/spring_2024_envs_research_amazon_ldas/main/resources/hybas_sa_lev05_areaofstudy.geojson"

# Open geojson url as geopanda dataframe
hybas_sa_lev05 = gpd.read_file(geojson_url) 


with urllib.request.urlopen(geojson_url) as url:
    jdata = json.loads(url.read().decode())

list_of_variables = [
    'Rainf_tavg', 'Qair_f_tavg', 'Qs_tavg',
    'Evap_tavg', 'SoilMoist_inst', 'SoilTemp_inst'
]

# Shiny App UI
app_ui = ui.page_fluid(
    ui.h1("Mapping - Forecast Data"),
    ui.hr(),
    ui.input_slider("time_index", "Select Time", 0, len(time) - 1, value=0, step=4),
    ui.input_radio_buttons("var_selector", "Select Variable", list_of_variables, selected="Rainf_tavg"),
    ui.input_radio_buttons(
        "profile_selector", "Select Depth Profile",
        choices={"0": "0-10cm", "1": "10-40cm", "2": "40-100cm", "3": "100-200cm"},
        selected="0"
    ),
    ui.hr(),
    ui.div(output_widget("map_plot"), style="display:inline-block; width:50%;"),
    ui.div(output_widget("box_plot"), style="display:inline-block; width:50%;"),
)

# Shiny Server
def server(input, output, session):
    # Reactive value for storing selected PFAF_ID
    selected_pfaf_id = reactive.Value(None)

    # Render the Map
    @output
    @render_plotly
    def map_plot():

        selected_var = ensemble_avg_dataset[input.var_selector()]
        selected_var = selected_var.fillna('')

        time_index = input.time_index()
        profile_index = int(input.profile_selector())

        # Create heatmap data
        if input.var_selector() == 'SoilMoist_inst':
            heatmap_data = selected_var.isel(time=time_index, SoilMoist_profiles=profile_index)
        elif input.var_selector() == 'SoilTemp_inst':
            heatmap_data = selected_var.isel(time=time_index, SoilTemp_profiles=profile_index)
        else:
            heatmap_data = selected_var.isel(time=time_index)

        # Create the heatmap
        fig = go.Figure(data=go.Heatmap(z=heatmap_data, x=longitude, y=latitude))

        # Add polygons from GeoJSON
        for feature in jdata['features']:
            pfaf_id = feature['properties']['PFAF_ID']
            if feature['geometry']['type'] == 'Polygon':
                x, y = zip(*feature['geometry']['coordinates'][0])
                fig.add_trace(go.Scatter(
                    x=x, y=y, mode='lines', line=dict(color='white', width=1.5),
                    text=[pfaf_id] * len(x), hoverinfo='text',
                    hovertemplate='PFAF_ID: %{text}<extra></extra>',
                    showlegend=False
                ))
            elif feature['geometry']['type'] == 'MultiPolygon':
                for polygon in feature['geometry']['coordinates']:
                    x, y = zip(*polygon[0])
                    fig.add_trace(go.Scatter(
                        x=x, y=y, mode='lines', line=dict(color='white', width=1.5),
                        text=[pfaf_id] * len(x), hoverinfo='text',
                        hovertemplate='PFAF_ID: %{text}<extra></extra>',
                        showlegend=False
                    ))

        # Finalize layout
        fig.update_layout(
            title=f"{input.var_selector()}",
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            height=600,
            width=800,
            margin=dict(l=0, r=0, t=30, b=0),
            clickmode='event+select'  # Enable click events
        )
        return fig

    # Update selected region on click
    @reactive.Effect
    @reactive.event(input["map_plot_click"])  # React to clicks on the map
    def update_selected_region():
        click_data = input["map_plot_click"]
        if click_data and 'points' in click_data:
            selected_pfaf_id.set(int(click_data['points'][0]['text']))

    # Render the Boxplot
    @output
    @render_plotly
    def box_plot():
        # Default PFAF_ID if none is selected
        pfaf_id = selected_pfaf_id.get() or 61581

        aoi = hybas_sa_lev05[hybas_sa_lev05.PFAF_ID == pfaf_id]

        #aoi = [feature for feature in jdata['features'] if feature['properties']['PFAF_ID'] == pfaf_id]

        """
        if not aoi:
            return go.Figure().update_layout(
                title=f"No data for PFAF_ID {pfaf_id}",
                height=600, width=800
            )
        """

        # Create the region mask
        mask = regionmask.mask_3D_geopandas(aoi, longitude, latitude)

        # Apply mask and summarize data
        variable = input.var_selector()
        masked_data = ensemble_members_dataset[variable].where(mask)
        summary = masked_data.groupby("time").mean(["north_south", "east_west"]).to_dataframe().reset_index()

        # Create the boxplot
        fig = go.Figure()
        fig.add_trace(go.Box(y=summary[variable], x= summary['time'].astype(str), name="Values", boxmean=True))

        # Finalize layout
        fig.update_layout(
            title=f"{variable} for PFAF_ID {pfaf_id}",
            xaxis_title="Time",
            yaxis_title=f"{variable}",
            height=600,
            width=800
        )
        return fig

# Create the Shiny app
app = App(app_ui, server)
