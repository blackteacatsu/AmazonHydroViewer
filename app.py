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
                ui.download_button('downloadData',  'Download'),
                fill=True
            ),

            ui.card(
                ui.card_header(ui.tags.h2('General forecast information')),
                ui.tags.p(
                    ui.tags.div('Ensemble forecasting - Instead of making a single forecast of the most ' \
                    'likely weather, a set (or ensemble) of forecasts  is  produced.  This  set  of ' \
                    'forecasts aims to give an indication of ' \
                    'the range of possible future states of ' \
                    'the atmosphere. ')
                )
            )
        ),
    ), full_width=True)

# --- Server logic ---#
def server(input, output, session):

    # Call Welcome message
    interface.info_modal()

    # Get the selected variable from the input
    def get_profile_key(var_selector):
        return {
            'SoilMoist_inst': 'SoilMoist_profiles',
            'SoilTemp_inst': 'SoilTemp_profiles'
        }.get(var_selector)
    
    # Filter the summary DataFrame by profile if applicable
    # This function checks if the variable has a profile dimension and filters accordingly
    def filter_by_profile(summary, var_selector, profile_selector):
        profile_col = get_profile_key(var_selector)
        if profile_col:
            return summary[summary[profile_col] == int(profile_selector)]
        return summary
    
    # Select the profile level from the dataset based on the variable and profile selector
    # This function retrieves the data for the selected variable and profile level
    def select_profile(data, var_selector, profile_selector):
        profile_dim = get_profile_key(var_selector)
        if profile_dim:
            return data.isel(
                time=input.time_slider(),
                **{profile_dim: int(profile_selector)}
            ).fillna("")
        else:
            return data.isel(time=input.time_slider()).fillna("")
        
    # Create a time slider for the time variable
    @output
    @render.ui
    def time_index_slider(): # create a time slider
        try :
            _, _, _, time = calculation.retrieve_data_from_remote(
                data_type=input.data_selector(),
                var=input.var_selector(),
                profile=input.profile_selector(),
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
            _, _, _, time = calculation.retrieve_data_from_remote(
                data_type=input.data_selector(),
                var=input.var_selector(),
                profile=input.profile_selector(),
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

        if input.data_selector() == 'Probabilistic':
            # Retrieve the dataset based on the selected variable and profile
            ds_forecast, lon, lat, _ = calculation.retrieve_data_from_remote(
                data_type=input.data_selector(),
                var=input.var_selector(),
                profile=input.profile_selector()
            )

            #print(ds_forecast)  # Debugging output

            for category_index in sorted(ds_forecast['category'].values):
                z_data = ds_forecast[input.var_selector()].isel(
                    time = input.time_slider(), 
                    category = category_index
                ).where(lambda x: x != 0)
                z_data = z_data.to_numpy()
                z_data = np.where(np.isnan(z_data), None, z_data)
                
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
        
        # If the dataset is not probabilistic, handle deterministic data
        ## Waiting to be implemented
        else: 
            selected_var_data = ds_ensemble_members[input.var_selector()].mean(dim="ensemble")
            ds_ensemble_members.close()

            if input.var_selector() == 'Streamflow_tavg':
                    selected_var_data = selected_var_data.where(selected_var_data <= 50, drop=True)
            
            z_data = select_profile(selected_var_data, input.var_selector(), input.profile_selector())

            return heatmapfig.add_trace(
                go.Heatmap(
                    z = z_data, 
                    x=lon, 
                    y=lat,
                    hoverinfo='skip'
                )
            )

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

        
        # When the user gives an input value by clicking
        else:
            #print(ds_ensemble_members) # Debugging output
            """summary = calculation.get_zonal_statistics(
                shared.hydrobasins_lev05_url,
                ds_ensemble_members, 
                int(polygon()),
                input.var_selector(), 
                lon, lat
            )
            ds_ensemble_members.close()"""

            #summary = filter_by_profile(summary, input.var_selector(), input.profile_selector())
            
            #print(summary)

            #x = sorted(summary['time'])
            #print(x)
            print(shared.raw_data_path + polygon() + ".csv")

            summary = pd.read_csv(
                shared.raw_data_path + polygon() + ".csv"
            )
            print(summary)  # Debugging output
            for t in sorted(summary['time'].unique()):
                data_for_t = summary.loc[summary['time'] == t, input.var_selector()]

                ensemblebox.add_trace(
                    go.Box(
                        y=data_for_t, x = [interface.format_date(t)] * len(data_for_t),
                        name=interface.format_date(t), #f"Cat {input.var_selector()} | {summary['time']}",  # This creates the legend label
                        marker_color=None,  # Let Plotly pick auto color
                        boxmean=True,  # Optional: show mean as a line
                    )
                )
            
            for t in sorted(summary['time'].unique()):
                # Filter the summary DataFrame for the current time index
                

                """
                for category_index in sorted(summary['category'].unique()):  

                    trace_data = summary[(summary['time'] == t) & (summary['category'] == category_index)]
                    #print(trace_data) # Debugging output

                    y_data = trace_data[input.var_selector()]

                    #print(y_data)

                    ensemblebox.add_trace(go.Box(
                        y=y_data,
                        x=[t]*len(y_data),
                        name=f"Cat {category_index} | {t}",  # This creates the legend label
                        marker_color=None,  # Let Plotly pick auto color
                        boxmean=True,  # Optional: show mean as a line
                        )
                    )
                """

            # Update layout with title and axis labels
            ensemblebox.update_layout(title = f'Displaying ensemble spread of {shared.list_of_variables.get(input.var_selector(), input.var_selector())} in over region {polygon()} @profile level {input.profile_selector()}')

        return ensemblebox

app=App(app_ui, server)