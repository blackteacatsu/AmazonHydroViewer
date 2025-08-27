from shiny import ui, render, App, reactive, Session
from shinywidgets import output_widget, render_plotly, register_widget
import xarray as xr
import plotly.graph_objects as go
import shared
import pandas as pd
import numpy as np
from modules import interface, mapping


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
                src="https://raw.githubusercontent.com/blackteacatsu/dokkuments/refs/heads/main/static/img/university_shield_blue.ico"
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
                fill=True,
            ),
            ui.card(
                ui.card_header(
                    ui.tags.h2(
                        "General forecast information \N{PUBLIC ADDRESS LOUDSPEAKER}"
                    )
                ),
                interface.build_general_info(),  #
                max_height="400px",
                full_screen=True,
            ),
        ),
    ),
    full_width=True,
)


# --- Server logic ---#
def server(input, output, session):

    # Call Welcome message
    # interface.info_modal()

    # Download
    # @output
    # @render.download
    # def downloadData():
    # return

    @reactive.Effect
    @reactive.event(input.var_selector)
    def _reset_depth_when_not_soil():
        if input.var_selector() not in ["SoilTemp_inst", "SoilMoist_inst"]:
            ui.update_select("depth_selector", selected=0)  # reset silently

    # Create a time slider for the time variable
    @output
    @render.ui
    def time_index_slider():  # create a time slider
        try:
            _, _, _, time = mapping.retrieve_data_from_remote(
                # data_type=input.data_selector(),
                var=input.var_selector(),
                profile=input.depth_selector(),
            )
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
            _, _, _, time = mapping.retrieve_data_from_remote(
                # data_type=input.data_selector(),
                var=input.var_selector(),
                profile=input.depth_selector(),
            )
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
        ds_forecast, lon, lat, _ = mapping.retrieve_data_from_remote(
            # data_type=input.data_selector(), # Currently only probabilistic is available
            var=input.var_selector(),
            profile=input.depth_selector(),
        )

        # print(ds_forecast)  # Debugging output

        for category_index in sorted(ds_forecast["category"].values):
            z_data = (
                ds_forecast[input.var_selector()]
                .isel(time=input.time_slider(), category=category_index)
                .where(lambda x: x != 0)
            )
            z_data = z_data.to_numpy()
            z_data = np.where(np.isnan(z_data), None, z_data)

            colorscale = shared.colorscales[category_index % len(
                shared.colorscales)]

            heatmapfig.add_trace(
                go.Heatmap(
                    z=z_data,
                    x=lon,
                    y=lat,
                    hoverinfo="skip",
                    name=shared.list_of_pcate.get(category_index),
                    colorbar=dict(
                        title=shared.list_of_pcate.get(category_index),
                        orientation="h",
                        yanchor="top",
                        len=0.75,
                        # x = 0.4, #+ 0.25 * category_index,
                        y=-0.2 - 0.2 * category_index,
                    ),
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

        # Initially display an empty figure
        if polygon() == "Waiting input":
            ensemblebox.update_layout(
                # title='Click on polygon to compute zonal average/maximum',
                annotations=[
                    dict(
                        text="No data selected, try clicking on a polygon",
                        xref="paper",
                        yref="paper",
                        x=0.5,
                        y=0.5,
                        showarrow=False,
                        font=dict(size=20, color="black"),
                    )
                ],
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
                annotations=[
                    dict(
                        text=f"Failed to load data; {e}",
                        xref="paper",
                        yref="paper",
                        x=0.5,
                        y=0.5,
                        showarrow=False,
                        font=dict(size=14),
                    )
                ],
                height=420,
            )
            return ensemblebox
        var = input.var_selector()
        depth = input.depth_selector()
        # var_col = f"{var}_lvl_{depth}" if var in ("SoilTemp_inst", "SoilMoist_inst") else var
        var_col = (f"{var}_lvl_{depth}" if input.var_selector()
                   in ["SoilTemp_inst", "SoilMoist_inst"] else var)

        # Store climatology for each time step
        climatology, time_labels = [], []
        # print(zonal_climatology_tab) # Debugging check

        for t in sorted(zonal_stats_tab["time"].unique()):
            # print(var_col)
            month = interface.format_date(t)
            data_for_t = zonal_stats_tab.loc[zonal_stats_tab["time"]
                                             == t, var_col]
            climatology_for_t = zonal_climatology_tab.loc[
                zonal_climatology_tab["month"] == int(month[-2:]), var_col
            ]  # .astype(float)

            # print(f'printing extracted climatology at time {t}\ {climatology_for_t}')
            # Save climatology for plotting later
            climatology.append(float(climatology_for_t))
            time_labels.append(month)

            ensemblebox.add_trace(
                go.Box(
                    y=data_for_t,
                    x=[interface.format_date(t)] * len(data_for_t),
                    name=interface.format_date(
                        t
                    ),  # f"Cat {input.var_selector()} | {summary['time']}",  # This creates the legend label
                    marker_color=None,  # Let Plotly pick auto color
                    boxmean=True,  # Optional: show mean as a line
                )
            )

        # print(f'printing finished climatology values list {climatology}')
        ensemblebox.add_trace(
            go.Scatter(
                y=climatology,
                x=time_labels,  # [interface.format_date(t)] * len(data_for_t),
                mode="lines+markers",
                # of {interface.format_date(t)[-2:]}", #f"Cat {input.var_selector()} | {summary['time']}",  # This creates the legend label
                name=f"(Climatology Mean)",
                # marker_color=None,  # Let Plotly pick auto color
                # boxmean=False,  # Optional: show mean as a line
                line=dict(color="black", dash="dot"),
                marker=dict(color="black", size=6),
            )
        )

        # Update layout with title and axis labels
        ensemblebox.update_layout(
            title=f"Displaying ensemble spread of {shared.list_of_variables.get(input.var_selector())} in region {polygon()} @depth {shared.list_of_profiles.get(int(input.depth_selector()))}",
            yaxis=dict(
                title=dict(
                    text=f"{shared.list_of_variables.get(input.var_selector())} ({shared.all_variable_units.get(input.var_selector())})"
                )
            ),
            legend=dict(
                orientation="h",
                x=0.5,
                xanchor="center",  # center horizontally
                y=-0.1,
                yanchor="top",  # place below the plot area
                # title_text=""            # optional: hide legend title if any
            ),
            # margin=dict(t=20, r=20, b=70, l=20)  # extra bottom space so it doesn't clip
        )

        return ensemblebox


app = App(app_ui, server)
