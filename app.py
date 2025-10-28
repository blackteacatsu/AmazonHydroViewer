from shiny import App, Inputs, Outputs, Session, reactive, ui, render
from shinywidgets import output_widget, render_plotly, register_widget
import xarray as xr
import plotly.graph_objects as go
import shared
import pandas as pd
import numpy as np
from modules import interface, mapping, plotly_theme


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
        # id = 'logo-top',
        # class_='navigation-logo'
    ),
    ui.tags.h1(shared.web_app_title),
    class_="header",
)

app_ui = ui.page_fluid(
    page_dependencies,
    page_header,
    # Add sidebar layout to the page
    ui.layout_sidebar(
        # Add contents to the side bar
        interface.build_sidebar_content(),

        # Defining the content outside the sidebar

        # ui.output_text_verbatim('selected_pfaf_id') # for debugging
        
        ui.layout_columns(
            ui.card(
                ui.card_header(ui.tags.h2(
                    "Map of the Amazon Basin \N{WORLD MAP}")),
                output_widget("heatmap"),
                class_="plotly-center-container",
            ),
            ui.card(
                ui.card_header(
                    ui.tags.h2(
                        "Click on polygon to see zonal statistics \N{MOUSE}")
                ),
                output_widget("boxplot"),
                full_screen=True,
            ),
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header(ui.tags.h2(
                    "Select Time \N{TEAR-OFF CALENDAR}")),
                ui.div(
                    ui.output_ui("time_index_slider"),
                    ui.output_text_verbatim("time_index"),
                    class_="center-control-content",
                ),
                # ui.download_button('downloadData',  'Download'),
                max_height="350px",
                fill=False,
            ),
            ui.card(
                ui.card_header(
                    ui.tags.h2(
                        "General forecast information \N{PUBLIC ADDRESS LOUDSPEAKER}"
                    )
                ),
                interface.build_general_info(),  #
                max_height="400px",
                full_screen=False,
            ),
        ),
    ),
    full_width=True,
)


# --- Server logic ---#
def server(input: Inputs, output: Outputs, session: Session):

    # Call Welcome message
    # interface.info_modal()

    # Download
    # @output
    # @render.download
    # def downloadData():
    # return
    
    @reactive.calc
    #@reactive.event(input.var_selector, input.depth_selector())
    def tempds():
        ds_forecast, lon, lat, time = mapping.retrieve_data_from_remote(var=input.var_selector(), profile=input.depth_selector())
        return ds_forecast, lon, lat, time

    # Create a time slider for the time variable
    @output
    @render.ui
    def time_index_slider():  # create a time slider
        try:
            _, _, _, time = tempds()
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
    def time_index():  # display current time index
        try:
            _, _, _, time = tempds()
            if time is None:
                return "No dataset loaded or time variable missing."
            current_time = input.time_slider()
            if current_time < 0 or current_time >= len(time):
                return "Invalid time index selected."

            return f"Currently at {interface.format_date(time[input.time_slider()].values)}"
        except Exception:
            return f"No dataset loaded or time variable missing."

    # Build the heatmap figure
    heatmapfig = mapping.buildregion(shared.hydrobasins_lev05_url)
    # Register the heatmap figure as a widget
    register_widget("heatmap", heatmapfig)

    # Handle click events on the heatmap polygon
    polygon = interface.on_polygon_click(heatmapfig.data[0])

    @reactive.effect
    def update_heatmap_figure():

        # Clear the previous heatmap trace (if it exists)
        if len(heatmapfig.data) > 1:
            # Keep only the first trace (polygon)
            heatmapfig.data = heatmapfig.data[:1]

        # Retrieve the dataset based on the selected variable and profile
        ds_forecast, lon, lat, _ = tempds()

        # print(ds_forecast)  # Debugging output

        for category_index in sorted(ds_forecast["category"].values):
            z_data = (
                ds_forecast[input.var_selector()]
                .isel(time=input.time_slider(), category=category_index)
                .where(lambda x: x != 0)
            )
            z_data = z_data.to_numpy()
            z_data = np.where(np.isnan(z_data), None, z_data)

            # Use pre-defined discrete colorscales for prob anomaly
            if input.var_selector() in ['Tair_f_tavg', 'SoilTemp_inst']:
                colorscale = shared.colorscales_discrete_temp[category_index]
            else:
                colorscale = shared.colorscales_discrete[category_index]

            heatmapfig.add_trace(
                go.Heatmap(
                    z=z_data,
                    x=lon,
                    y=lat,
                    hoverinfo="skip",
                    name=shared.list_of_pcate.get(category_index),
                    colorbar={
                        **plotly_theme.get_colorbar_style(
                            shared.list_of_pcate.get(category_index)
                        ),
                        'y': -0.2 - 0.2 * category_index,
                        'tickmode': 'array',
                        'tickvals': [40, 50, 60, 70, 80, 90, 100],
                        'ticktext': ['40', '50', '60', '70', '80', '90', '100'],
                    },
                    colorscale=colorscale,
                    zmin=40,
                    zmax=100,
                )
            )
        return heatmapfig

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
                shared.raw_data_path + polygon() + ".csv")
            zonal_climatology_tab = pd.read_csv(
                shared.climatology_data_path + polygon() + ".csv"
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
                    name=month,  # This creates the legend label
                    marker_color=None,  # Let Plotly pick auto color
                    boxpoints=False,  # Turn off individual points
                    hoverinfo='x + y',  # Show only y-axis values in hover
                )
            )

        # print(f'printing finished climatology values list {climatology}')
        ensemblebox.add_trace(
            go.Scatter(
                y=climatology,
                x=time_labels,  # [interface.format_date(t)] * len(data_for_t),
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
        var_name = shared.list_of_variables.get(input.var_selector()).upper()
        var_unit = shared.all_variable_units.get(input.var_selector())
        depth_label = shared.list_of_profiles.get(int(input.depth_selector()))

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


app = App(app_ui, server)
