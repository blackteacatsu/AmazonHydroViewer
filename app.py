from shiny import App, Inputs, Outputs, Session, reactive, ui, render
from pathlib import Path
from shinywidgets import output_widget, render_plotly, render_widget
import plotly.graph_objects as go
import shared
import pandas as pd
from ipyleaflet import TileLayer
from modules import interface, plotly_theme
from ipyleaflet import Map, basemaps, TileLayer, GeoJSON, WidgetControl, LayersControl, basemap_to_tiles, FullScreenControl
from ipywidgets import HTML
import requests

# Shared local tile server URL
TILE_SERVER_URL = "http://localhost:4000"

# --- Setup page ui ---#

# Build <head> contents
page_dependencies = ui.head_content(
    ui.include_css("styles.css"),
    ui.tags.link(
        rel="icon",
        type="image/x-icon",
        href="https://raw.githubusercontent.com/blackteacatsu/dokkuments/refs/heads/main/static/img/university_shield_blue.ico",
    ),
    ui.tags.title("Amazon HydroViewer"),
    ui.tags.meta(name="apple-mobile-web-app-status-bar-style",
                 content="#000000"),
    ui.tags.meta(name="apple-mobile-web-app-capable", content="yes"),
)

page_header = ui.tags.div(
    ui.tags.div(
        ui.tags.a(
            ui.tags.img(
                src="https://raw.githubusercontent.com/blackteacatsu/dokkuments/refs/heads/main/static/img/university.shield.blue.svg"
            ),
            href="https://pages.jh.edu/bzaitch1/",
        ),
    ),
    ui.tags.h1('Hydrometeorology of The Amazon Basin'),
    class_="header",
)

r = requests.get(shared.hydrobasins_lev05_url)
geojson_data = r.json()

# Define page content and interface structure
app_ui = ui.page_fluid(
    page_dependencies,
    page_header,
    # Add sidebar layout to the page
    ui.layout_sidebar(
        # Add contents to the side bar
        interface.build_sidebar_content(),

        # Defining the content outside the sidebar 
        ui.layout_columns(
            ui.card(
                ui.card_header(ui.tags.h2(
                    "Map of the Amazon Basin \N{ROUND PUSHPIN}")),
                output_widget("heatmap"),
                class_="plotly-center-container", full_screen = True
            ),
            ui.card(
                ui.card_header(
                    ui.tags.h2(
                        "Zonal statistics \N{INBOX TRAY}")
                ),
                output_widget("boxplot"),
                full_screen=False,
            ),
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header(ui.tags.h2(
                    "Select Time \N{TEAR-OFF CALENDAR}")),
                ui.div(
                    ui.output_ui("time_step_slider"),
                    ui.output_text_verbatim("time_index"),
                    class_="center-control-content",
                ),
                max_height="350px",
                fill=False,
            ),
            ui.card(
                ui.card_header(
                    ui.tags.h2(
                        "General forecast information \N{PUBLIC ADDRESS LOUDSPEAKER}"
                    )
                ),
                interface.build_general_info(), 
                max_height="400px",
                full_screen=False,
            ),
        ),
    ),
    full_width=True,
)


# --- Server logic ---#
def server(input: Inputs, output: Outputs, session: Session):
    
    polygon = reactive.value('Waiting input')

    # Get time index 
    @reactive.calc
    def get_time_steps():
        """Get time steps from tile server metadata endpoint."""
        try:
            variable = input.var_selector()
            if not variable:
                return None
            profile = int(input.depth_selector()) if variable in ["SoilTemp_inst", "SoilMoist_inst"] else 0

            res = requests.get(
                f"{TILE_SERVER_URL}/pyramid/time/{variable}",
                params={"profile": profile},
                timeout=10,
            )
            if res.status_code != 200:
                return None
            payload = res.json()
            time_values = payload.get("time", [])
            return time_values if time_values else None
        except Exception:
            return None

    # Create a time slider to pick time-dimension
    @output
    @render.ui
    def time_step_slider():  # create a time slider
        try:
            time = get_time_steps()
            if time is None:
                return ui.div("No dataset loaded or time variable missing.")

            if time is not None:  # check if time variable exists
                return ui.input_slider(
                    "time_slider",
                    "Select forecast lead time (in month)",
                    min=0,
                    max=len(time) - 1,
                    animate=True,
                    step=1,
                    value=0,
                    ticks=True,
                )

        except Exception as e:
            return ui.div("No dataset loaded or time variable missing.")
    
    # Display the current time index
    @output
    @render.text
    def time_index():
        try:
            time = get_time_steps()
            if time is None:
                return "No dataset loaded or time variable missing."
            current_time = input.time_slider()
            if current_time < 0 or current_time >= len(time):
                return "Invalid time index selected."

            return f"Currently at {interface.format_date(time[input.time_slider()])}"
        except Exception:
            return "No dataset loaded or time variable missing."
    
    @render_widget
    def heatmap():
        """Update tile layer when tile URL changes"""
        variable = input.var_selector()
        if not variable:
            return None
        category = int(input.forecast_category_selector())
        profile = int(input.depth_selector()) if variable in ["SoilTemp_inst", "SoilMoist_inst"] else 0
        try:
            time_idx = input.time_slider()
            if time_idx is None:
                return None
        except Exception:
            return None

        if variable in ['Tair_f_tavg', 'SoilTemp_inst']:
            colormap = shared.colorscales_temp.get(input.forecast_category_selector())

        else:
           colormap = shared.colorscales.get(input.forecast_category_selector())

        tile_url = (f'{TILE_SERVER_URL}/tiles/{variable}/{time_idx}/{category}/'
                    f'{{z}}/{{x}}/{{y}}.png?colormap={colormap}&profile={profile}'
                    f'&mode=global&vmin=40&vmax=100'
        )

        # tile_url, variable, category = build_tile_url()
        print(f"{variable, category}")
        print(tile_url)

        forecast_layer = TileLayer(
                url=tile_url,
                name=f"{variable} - Category {category}",
                opacity=0.8,
                attribution='HydroViewer',
                min_native_zoom=4,
                max_native_zoom=9,
                tms=True,
        )

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
        #m.add_layer(polygon_layer)
        #m.add_layer(forecast_layer)

        m = Map(
            center=[-7, -66],
            zoom=4,
            scroll_wheel_zoom=True,
            max_zoom = 9,
            basemap = basemap_to_tiles(basemaps.Stadia.AlidadeSmoothDark, 
                                       "CartoDB Positron") #Stadia.AlidadeSmooth
        )

        layercontrol = LayersControl(position='bottomright')
        m.add_control(layercontrol)

        m.add_layer(polygon_layer)
        m.add_layer(forecast_layer)

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

        def on_polygon_click(event, feature, **kwargs):
            if feature and "properties" in feature:
                pfaf_id = feature["properties"].get("PFAF_ID")
                if pfaf_id is not None:
                    #print(pfaf_id)
                    polygon.set(str(pfaf_id))
                    print(polygon())

        polygon_layer.on_click(on_polygon_click)
        # print(f'Map Widget layer updated: # of layers currently loaded is {len(heatmapfig.layers)}')
        # for layer in m.layers:
        #   print(f'  - {layer.name}')
        #m.add(FullScreenControl())
        
        return m
    


    # Build the boxplot figure which will display the zonal statistics
    @render_plotly
    def boxplot():
        ensemblebox = go.Figure()

        # Initially display an empty figure with Brutalist styling
        if polygon() == "Waiting input":
            ensemblebox.update_layout(
                **plotly_theme.get_brutalist_layout(
                    annotations=[
                        plotly_theme.get_empty_state_annotation(
                            "NO DATA SELECTED<br>CLICK ON A POLYGON TO VIEW STATISTICS"
                        )
                    ]
                )
            )
            return ensemblebox

        try:
            zonal_stats_tab = pd.read_csv(
                shared.ZONAL_FORECAST_PATH + polygon() + ".csv")
            zonal_climatology_tab = pd.read_csv(
                shared.ZONAL_CLIM_PATH + polygon() + ".csv"
            )
        except Exception as e:
            ensemblebox.update_layout(
                **plotly_theme.get_brutalist_layout(
                    annotations=[
                        plotly_theme.get_empty_state_annotation(
                            f"ERROR LOADING DATA<br>{str(e)}"
                        )
                    ],
                    height=420,
                )
            )
            return ensemblebox
        var = input.var_selector()
        depth = input.depth_selector()
        var_col = (f"{var}_lvl_{depth}" if input.var_selector() in ["SoilTemp_inst", "SoilMoist_inst"] else var)

        # Store climatology for each time step
        climatology, time_labels = [], []
        # print(zonal_climatology_tab) # Debugging check

        for t in sorted(zonal_stats_tab["time"].unique()):
            # print(var_col) # Debugging line
            month = interface.format_date(t)
            data_for_t = zonal_stats_tab.loc[zonal_stats_tab["time"]== t, var_col]
            climatology_for_t = zonal_climatology_tab.loc[zonal_climatology_tab["month"] == int(month[-2:]), var_col] 
            # print(f'printing extracted climatology at time {t}\ {climatology_for_t}') # Debugging line

            # Save climatology for plotting later
            climatology.append(float(climatology_for_t.iloc[0]))
            time_labels.append(month)

            # Add forecast data to box plot for this time step
            ensemblebox.add_trace(
                go.Box(
                    y=data_for_t,
                    x= [month] * len(data_for_t),
                    name=month,  
                    marker_color=None,  # Let Plotly pick auto color
                    boxpoints=False,  
                    hoverinfo='x + y',  # Show only y-axis values in hover
                )
            )

        # print(f'printing finished climatology values list {climatology}')
        ensemblebox.add_trace(
            go.Scatter(
                y=climatology,
                x=time_labels, 
                mode="lines+markers",
                name=f"(Climatology Mean)",
                # marker_color=None,  # Let Plotly pick auto color
                # boxmean=False,  # Optional: show mean as a line
                line=dict(color="black", dash="dot"),
                marker=dict(color="black", size=6),
                hovertemplate='<b>Climatology</b><br>%{x}<br>Mean: %{y}<extra></extra>',
            )
        )

        # Apply Brutalist theme with custom title and axis labels
        var_name = shared.CLIM_VAR_META.get(input.var_selector())['long_name'].upper()
        var_unit = shared.CLIM_VAR_META.get(input.var_selector())['unit']
        depth_label = shared.SOIL_VAR_PROFILE.get(int(input.depth_selector()))

        ensemblebox.update_layout(
            **plotly_theme.get_brutalist_layout(
                title={
                    'text': f"ENSEMBLE SPREAD: {var_name} | REGION {polygon()} | DEPTH {depth_label}",
                },
                xaxis={
                    'title': {'text': 'TIME PERIOD'},
                    'showgrid': False,
                },
                yaxis={
                    'title': {'text': f"{var_name} ({var_unit})"},
                },
            )
        )

        return ensemblebox


app = App(app_ui, server, static_assets=Path(__file__).parent / "www")
