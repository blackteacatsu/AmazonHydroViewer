from shiny import ui, render, App, reactive, Session
from shinywidgets import output_widget, render_plotly, register_widget
import xarray as xr
import plotly.graph_objects as go
import shared
import pandas as pd
import numpy as np
from modules import calculation, interface, mapping


# --- Setup page ui ---#

# Build <head> contents
page_dependencies = ui.head_content(
    ui.include_css("styles.css"),
    ui.tags.link(rel="icon", type='image/x-icon', href='https://raw.githubusercontent.com/blackteacatsu/dokkuments/refs/heads/main/static/img/university_shield_blue.ico'),
    ui.tags.title('Amazon HydroViewer'),
    ui.tags.meta(name="apple-mobile-web-app-status-bar-style", content="#000000"),
    ui.tags.meta(name="apple-mobile-web-app-capable", content="yes"),
)

page_header = ui.tags.div(
    ui.tags.div(
        ui.tags.a(
            ui.tags.img(src='https://raw.githubusercontent.com/blackteacatsu/dokkuments/refs/heads/main/static/img/university_shield_blue.ico'),
            href='https://pages.jh.edu/bzaitch1/'
        ),
        #id = 'logo-top',
        #class_='navigation-logo'
    ),
    ui.tags.h1(shared.web_app_title),
    class_ = 'header'
)

app_ui = ui.page_fluid(
    page_dependencies,
    page_header,

    # Add sidebar layout to the page
    ui.layout_sidebar(    
        # Add contents to the side bar
        interface.build_sidebar_content(),

        # Defining the content outside the sidebar
        #ui.output_text_verbatim('selected_pfaf_id') # for debugging
        ui.layout_columns(
            ui.card(
                ui.card_header(ui.tags.h2("Map of the Amazon Basin \N{World Map}")),
                output_widget('heatmap'), class_='plotly-center-container'),

            ui.card(
                ui.card_header(ui.tags.h2("Click on polygon to see zonal statistics \N{Mouse}")),
                output_widget('boxplot'), full_screen=True)
        ),
        
        ui.layout_columns(
            ui.card(
                ui.card_header(ui.tags.h2("Select Time \N{Tear-Off Calendar}")),

                ui.div(
                    ui.output_ui('time_index_slider'),
                    ui.output_text_verbatim("time_index"),
                    class_='center-control-content'),
                #ui.download_button('downloadData',  'Download'),
                fill=True
            ),

            ui.card(
                ui.card_header(ui.tags.h2('General forecast information \N{Public Address Loudspeaker}')),
                interface.build_general_info(), # 
                max_height='400px', full_screen=True

            )
        )
    ), full_width=True)

# --- Server logic ---#
def server(input, output, session):

    # Call Welcome message
    interface.info_modal()

    # Download
    #@output
    #@render.download
    #def downloadData():
        #return 
    """
    # Get the selected variable from the input
    def get_profile_key(var_selector):
        return {
            'SoilMoist_inst': 'SoilMoist_profiles',
            'SoilTemp_inst': 'SoilTemp_profiles'
        }.get(var_selector)
    
    # Filter the summary DataFrame by profile if applicable
    def filter_by_profile(summary, var_selector, profile_selector):
        profile_col = get_profile_key(var_selector)
        if profile_col:
            return summary[summary[profile_col] == int(profile_selector)]
        return summary
    
    # Select the profile level from the dataset based on the variable and profile selector
    def select_profile(data, var_selector, profile_selector):
        profile_dim = get_profile_key(var_selector)
        if profile_dim:
            return data.isel(
                time=input.time_slider(),
                **{profile_dim: int(profile_selector)}
            ).fillna("")
        else:
            return data.isel(time=input.time_slider()).fillna("")
    """

    @output
    @render.ui
    def profile_selector():
        if input.var_selector() in ['SoilMoist_inst', 'SoilTemp_inst']:
            return ui.input_select(
                "select_depth",
                "Select depth lvl.", 
                choices=shared.list_of_profiles, 
                selected=0)

    # Create a time slider for the time variable
    @output
    @render.ui
    def time_index_slider(): # create a time slider
        try :
            _, _, _, time = mapping.retrieve_data_from_remote(
                #data_type=input.data_selector(),
                var=input.var_selector(),
                profile=input.select_depth() if input.var_selector() in ['SoilMoist_inst', 'SoilTemp_inst'] else 0
            )
            if time is None:
                return ui.div("No dataset loaded or time variable missing.")
            
            if time is not None: # check if time variable exists
                return ui.input_slider(
                    "time_slider",
                    "Select forecast lead time (in month)",
                    min=0, 
                    max=len(time)-1,
                    animate=True, 
                    step=1, 
                    value=0,
                    ticks=True)
        
        except Exception as e:
            return ui.div("No dataset loaded or time variable missing.")
    
    # Display the current time index
    @output
    @render.text
    def time_index(): # display current time index
        try:
            _, _, _, time = mapping.retrieve_data_from_remote(
                #data_type=input.data_selector(), # removed for now
                var=input.var_selector(),
                profile=input.select_depth() if input.var_selector() in ['SoilMoist_inst', 'SoilTemp_inst'] else 0
            )
            if time is None:
                return "No dataset loaded or time variable missing."
            current_time = input.time_slider()
            if current_time <0 or current_time >= len(time):
                return "Invalid time index selected."
            
            return f"Currently at {interface.format_date(time[input.time_slider()].values)}"
        except Exception as e:
            return "No dataset loaded or time variable missing."
        
    # Build the heatmap figure
    heatmapfig = mapping.buildregion(shared.hydrobasins_lev05_url)
    # Register the heatmap figure as a widget
    register_widget('heatmap', heatmapfig)

    # Handle click events on the heatmap polygon
    polygon = interface.on_polygon_click(heatmapfig.data[0])

    @reactive.effect
    def update_heatmap_figure():
        # Clear the previous heatmap trace (if it exists)
        if len(heatmapfig.data) > 1:
            heatmapfig.data = heatmapfig.data[:1]  # Keep only the first trace (polygon)

        # Retrieve the dataset based on the selected variable and profile
        ds_forecast, lon, lat, _ = mapping.retrieve_data_from_remote(
            #data_type=input.data_selector(), # removed for now
            var=input.var_selector(),
            profile=input.select_depth() if input.var_selector() in ['SoilMoist_inst', 'SoilTemp_inst'] else 0
        ) 

        #print(ds_forecast)  # Debugging output

        for category_index in sorted(ds_forecast['category'].values):
            z_data = ds_forecast[input.var_selector()].isel(
                time = input.time_slider(), 
                category = category_index
            ).where(lambda x: x != 0)
            z_data = z_data.to_numpy()
            z_data = np.where(
                np.isnan(z_data), None, z_data)
            
            colorscale = shared.colorscales[category_index % len(shared.colorscales)]

            heatmapfig.add_trace(
                go.Heatmap(
                    z=z_data, x=lon, 
                    y=lat, hoverinfo='skip', 
                    name=shared.list_of_pcate.get(category_index), 
                    colorbar=dict(
                        title = shared.list_of_pcate.get(category_index),
                        orientation = 'h',
                        yanchor="top", len=0.75,
                        #x = 0.4, #+ 0.25 * category_index,
                        y = -0.2 - 0.2 * category_index
                    ), 
                colorscale=colorscale, zmin=40, zmax=100
                )
            )
        return heatmapfig
        
    # Build the boxplot figure which will display the zonal statistics
    @render_plotly
    def boxplot():
        ensemblebox = go.Figure()

        # Initially display an empty figure
        if polygon() == 'Waiting input': 
            ensemblebox.update_layout(
                #title='Click on polygon to compute zonal average/maximum',
                annotations =[
                    dict(
                        text='No data selected, try clicking on a polygon',
                        xref='paper', yref='paper',
                        x=0.5, y=0.5,
                        showarrow=False,
                        font=dict(size=20, color='black')
                    )
                ],
            )
            return ensemblebox

        var = input.var_selector()
        depth = input.select_depth()
        var_col = f"{var}_lvl_{depth}" if var in ("SoilTemp_inst", "SoilMoist_inst") else var

        # When the user gives an input value by clicking
        try:
            zonal_stats_tab = pd.read_csv(shared.raw_data_path + polygon() + ".csv")
            zonal_climatology_tab = pd.read_csv(shared.climatology_data_path + polygon() + ".csv")
        except Exception as e:
            ensemblebox.update_layout(
                        annotations=[dict(
                            text=f"Failed to load data; {e}",
                            xref="paper", yref="paper", x=0.5, y=0.5,
                            showarrow=False, font=dict(size=14)
                        )],
                        height=420
                    )
            return ensemblebox

        #print(zonal_climatology_tab)
        # Store climatology for each time step
        climatology, time_labels = [], []
        
        for t in sorted(zonal_stats_tab['time'].unique()):
            time_label = interface.format_date(t)
            y = zonal_stats_tab.loc[zonal_stats_tab["time"] == t, var_col].astype(float).dropna()
            if y.empty:
                continue
            # Use a single scalar per month for the overlay line
            month = int(time_label[-2:])
            clim_val = zonal_climatology_tab.loc[zonal_climatology_tab['month'] == month, var_col].astype(float).dropna()
            #float(zonal_climatology_tab.get(month))
            time_labels.append(time_label)
            climatology.append(clim_val)
            
            """if input.var_selector() in ['SoilTemp_inst', 'SoilMoist_inst']: # check if variable is soil temperature or moisture
                data_for_t = zonal_stats_tab.loc[zonal_stats_tab['time'] == t, input.var_selector() + "_lvl_" + input.select_depth()]
                climatology_for_t = zonal_climatology_tab.loc[zonal_climatology_tab['month'] == int(interface.format_date(t)[-2:]), input.var_selector() + "_lvl_" + input.select_depth()]
                climatology.append(climatology_for_t)
                time_labels.append(interface.format_date(t))

            else: 
                data_for_t = zonal_stats_tab.loc[zonal_stats_tab['time'] == t, input.var_selector()]
                climatology_for_t = zonal_climatology_tab.loc[zonal_climatology_tab['month'] == int(interface.format_date(t)[-2:]), input.var_selector()]
                climatology.append(climatology_for_t)
                time_labels.append(interface.format_date(t))"""
            
            # Save climatology for plotting later
            #print(climatology_for_t)
            

            # print(interface.format_date(t)[-2:])
            # print(climatology_for_t) # Debug output

            ensemblebox.add_trace(
                    go.Box(
                        y=y,
                        x = [time_label] * len(y),
                        name=interface.format_date(t), #f"Cat {input.var_selector()} | {summary['time']}",  # This creates the legend label
                        marker_color=None,  # Let Plotly pick auto color
                        boxmean=True,  # Optional: show mean as a line
                    )
                )
        print(time_labels)
        #print(climatology)
        ensemblebox.add_trace(
            go.Scatter(
                y=zonal_climatology_tab[var_col], 
                x = time_labels, #[interface.format_date(t)] * len(data_for_t),
                mode="lines+markers",
                name=f"(Climatology Mean)", #of {interface.format_date(t)[-2:]}", #f"Cat {input.var_selector()} | {summary['time']}",  # This creates the legend label
                #marker_color=None,  # Let Plotly pick auto color
                #boxmean=False,  # Optional: show mean as a line
                line=dict(color="black", dash="dot"),
                marker=dict(color="black", size=6) 
            )
        )
            
        # Update layout with title and axis labels
        ensemblebox.update_layout(title = f'Displaying ensemble spread of {shared.list_of_variables.get(input.var_selector(), input.var_selector())} in over region {polygon()} @profile level {input.select_depth()}',
                                    yaxis = dict(title = dict(text = f'{shared.list_of_variables.get(input.var_selector())} ({shared.all_variable_units.get(input.var_selector())})'))
                                    )

        return ensemblebox

app=App(app_ui, server)