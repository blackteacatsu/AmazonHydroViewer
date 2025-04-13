from shiny import ui, render, App, reactive, Session
from shinywidgets import output_widget, render_plotly, register_widget
import xarray as xr
import plotly.express as px
import plotly.graph_objects as go

import shared

from modules import calculation, interface, mapping


# --- Setup page ui ---#

# Build <head> contents
page_dependencies = ui.head_content(
    ui.include_css(shared.css_file_path),
    ui.tags.link(rel="icon", type='image/x-icon', href='https://raw.githubusercontent.com/blackteacatsu/dokkuments/refs/heads/main/static/img/university_shield_blue.ico'),
    ui.tags.title('Amazon HydroViewer'),
    ui.tags.meta(name="apple-mobile-web-app-status-bar-style", content="#000000"),
    ui.tags.meta(name="apple-mobile-web-app-capable", content="yes"),
)

page_header = ui.tags.div(
    ui.tags.div(
        ui.tags.a(
            ui.tags.img(src='https://raw.githubusercontent.com/blackteacatsu/servir_dashboard_shiny/refs/heads/main/dump/datavisualization/assets/university_shield_blue_iiL_icon.ico'),
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
        #ui.output_text_verbatim('selected_pfaf_id'),
        ui.layout_columns(
            ui.card(
                ui.card_header(ui.tags.h2("Map of the Amazon Basin \N{World Map}")),
                output_widget('heatmap')),

            ui.card(
                ui.card_header(ui.tags.h2("Click on polygon to compute zonal average/maximum")),
                output_widget('boxplot'))
                ),
            
        ui.card( {"style": "width: 360px"},
            ui.card_header(ui.tags.h2("Select Time \N{Tear-Off Calendar}")),
            ui.row(ui.output_ui('time_index_slider'),
                   ui.output_text_verbatim("time_index")),
                fill=True,)
        ),
full_width=True)


def server(input, output, session):

    @reactive.calc
    def redirect_nc_file():
        if input.data_selector() =='Deterministic':
            if input.var_selector() == 'Streamflow_tavg':
                return xr.open_dataset(shared.routing_ensemble_members_path)
            else:
                return xr.open_dataset(shared.surface_ensemble_members_path)
        else:
            print(str(shared.probabilistic_data_path))
            return xr.open_dataset(str(shared.probabilistic_data_path) + f'\prob2024_12_31tercile_probability_max_{input.var_selector()}.nc')
    
    @output
    @render.ui
    def time_index_slider():
        ds_ensemble_members = redirect_nc_file()
        _, _, time = mapping.get_standard_coordinates(ds_ensemble_members)

        if time is not None:
            return ui.input_slider(
                "time_slider", 
                "Move the slider below to switch time instance", 
                min=0, 
                max=len(time)-1,
                animate=True, 
                step=1, 
                value=0,
                ticks=True,
                time_format='2024-08-31 00:00:00')
        return ui.div("No dataset loaded or time variable missing.")

    @output
    @render.text
    def time_index():
        ds_ensemble_members = redirect_nc_file()
        _, _, time = mapping.get_standard_coordinates(ds_ensemble_members)
        return f"{interface.format_date(time[input.time_slider()].values)}"

    heatmapfig = mapping.buildregion(shared.hydrobasins_lev05_url)
    register_widget('heatmap', heatmapfig)
    polygon = interface.on_polygon_click(heatmapfig.data[0])

    @reactive.effect
    def update_heatmap_figure():
        ds_ensemble_members = redirect_nc_file()
        lon, lat, _ = mapping.get_standard_coordinates(ds_ensemble_members)

        selected_var_data = ds_ensemble_members[input.var_selector()].mean(dim="ensemble")
        ds_ensemble_members.close()
        #print(selected_var_data)

        # Clear the previous heatmap trace (if it exists)
        if len(heatmapfig.data) > 1:
            heatmapfig.data = heatmapfig.data[:1]  # Keep only the first trace (polygon)

        #print(input.time_slider())
        if input.var_selector() == 'SoilMoist_inst':
            z_data = selected_var_data.isel(time = input.time_slider(), SoilMoist_profiles = int(input.profile_selector())).fillna("")

        elif input.var_selector() == 'SoilTemp_inst':
            z_data = selected_var_data.isel(time = input.time_slider(), SoilTemp_profiles = int(input.profile_selector())).fillna("")

        else:
            if input.var_selector() == 'Streamflow_tavg':
                selected_var_data = selected_var_data.where(selected_var_data <= 50, drop=True)
            z_data = selected_var_data.isel(time = input.time_slider()).fillna("")

        heatmapfig.add_trace(
            go.Heatmap(z = z_data, 
                        x=lon, 
                        y=lat,
                        hoverinfo='skip'
            )
        )  
    
    # Boxplot 
    @render_plotly
    def boxplot():
        ds_ensemble_members = redirect_nc_file()
        lon, lat, _ = mapping.get_standard_coordinates(ds_ensemble_members)

        ensemblebox = go.Figure()

        # Initially display an empty figure
        if polygon() == 'Waiting input': 
            ensemblebox.update_layout(
                xaxis = dict(visible=False), 
                yaxis=dict(visible=False), 
                annotations = [dict(
                text=f"{polygon()}",
                showarrow=False,
                font=dict(size=16),
                align='center'
                )]
        
            )
        
        # When the user gives an input value by clicking
        else:
            #print(input.var_selector())
            summary = calculation.get_zonal_statistics(shared.hydrobasins_lev05_url, 
                                                               ds_ensemble_members, 
                                                               int(polygon()), 
                                                               input.var_selector(), 
                                                               lon, lat)
            ds_ensemble_members.close()

            if input.var_selector() == 'SoilMoist_inst': # handler if user select soil moisture
                summary  = summary[summary["SoilMoist_profiles"] == int(input.profile_selector())]
            
            elif input.var_selector() == 'SoilTemp_inst': # handler if user select soil temperature
                summary  = summary[summary["SoilTemp_profiles"] == int(input.profile_selector())]
            
            # Loop through unique times to assign auto colors
            for t_idx, t in enumerate(sorted(summary['time'].unique())):
                trace_data = summary[summary['time'] == t]
                ensemblebox.add_trace(go.Box(
                    y=trace_data[input.var_selector()],
                    name=str(t),  # This creates the legend label
                    marker_color=None,  # Let Plotly pick auto color
                    boxmean=True  # Optional: show mean as a line
                ))
            
            ensemblebox.add_trace(go.Box(y=summary[input.var_selector()], 
                                         x = summary['time'], 
                                         #color=summary['time'], 
                                         text=f'Displaying zonal average in {polygon()} @profile level {input.profile_selector()}'))
        return ensemblebox

"""
                return px.box(summary, 
                              y=input.var_selector(), 
                              x = 'time', color='time', 
                              title=f'Displaying zonal average in {polygon()} @profile level {input.profile_selector()}')
                
            else:
                return go.Box(
                              y=summary[input.var_selector()], 
                              x = summary['time'], 
                              name=summary['time'], 
                              title=f'Displaying spread of ensemble members averaged for zone {polygon()}')
""" 
app=App(app_ui, server)