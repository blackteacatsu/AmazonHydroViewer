from shiny import ui, reactive
import shared

"""
Generate buttons in the sidebar 
"""
def build_sidebar_content():
    return ui.sidebar( 
        # Buttons to select variable
        ui.input_radio_buttons(
            "var_selector", 
            "Select your variable below", 
            choices=shared.list_of_variables, 
            selected='Rainf_tavg'),

        # Buttons to select profile
        ui.input_select(
            "profile_selector", 
            "Depth (Only applicable to soil temperature & moisture)", 
            choices=shared.list_of_profiles, 
            selected=0),

        # Buttons to select data type
        ui.input_radio_buttons(
            "data_selector", 
            "Select your data type", 
            choices=['Deterministic', 'Probabilistic'], 
            selected='Deterministic'),
        
        # Url portal to documentation 
        ui.a('Take me to documentation \N{Page with Curl}', 
             href = shared.documentation_site_url, 
             target='_blank', 
             class_="btn btn-primary"),
        # 
        ui.popover(ui.a('About this page', class_="btn btn-primary"),'Welcome! \n This interactive map provides access to estimates of monthly meteorological and hydrological conditions in the Amazon basin, derived from output of a Land Data Assimilation System. The original implementation is described in Recalde et al. (2022). The current, updated system is maintained by Dr. Prakrut Kansara, with visualizations designed by Kris Su. It is supported by a NASA SERVIR award. Please direct questions to Ben Zaitchik (zaitchik@jhu.edu).')
        )

"""
Define callback function that captures user's cursor click on map
"""
def on_polygon_click(trace):
    # Reactive value to store selected PFAF_ID
    clicked_pfaf_id = reactive.Value('Waiting input')

    # Define callback function
    def on_mouse_click(trace, points, selector):
        if points.point_inds:
            clicked_index = points.point_inds[0]
            clicked_pfaf_id.set(trace.text[clicked_index])
    
    # Attach the click handler to the polygon trace
    trace.on_click(on_mouse_click)
    return clicked_pfaf_id

"""
Create a function to format the datetime values
"""
def format_date(datetime_value):
    return str(datetime_value)[:7]  # Keep the month part

"""
Create a welcome modal message
"""
def _():
    m = ui.modal(
        f'This interactive map provides access to estimates of monthly meteorological and hydrological conditions in the Amazon basin, derived from output of a <a href="https://{new_test}">text of the link</a>. The original implementation is described in Recalde et al. (2022).',
        title='Welcome !'
    )