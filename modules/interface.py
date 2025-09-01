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
            "Select variables below:", 
            choices=shared.list_of_variables, 
            selected='Rainf_tavg'),

        # Buttons to select profile
        ui.panel_conditional(
            "input.var_selector == 'SoilMoist_inst' || input.var_selector == 'SoilTemp_inst'", 
            ui.input_select(
                "depth_selector", 
                "Depth (Only applicable to soil temperature & moisture)", 
                choices=shared.list_of_profiles, 
                selected=0
            ),
        ),

        # Buttons to select data type
        #ui.input_radio_buttons(
            #"data_selector", 
            #"Select forecast type:", 
            #choices=['Probabilistic'], # 'Deterministic' 
            #selected='Probabilistic')""",
        
        # Url portal to documentation 
        ui.a('Take me to documentation \N{Page with Curl}', 
             href = "https://blackteacatsu.github.io/dokkuments/blog/welcome", 
             target='_blank', 
             class_="btn btn-primary"),

        # Url portal to GitHub data repository
        ui.a('Take me to data \N{Page with Curl}', 
             href = "https://github.com/Amazon-ARCHive/amazon_hydroviewer_backend/tree/main", 
             target='_blank', 
             class_="btn btn-primary"), open='closed' # for debugging and test purposes
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
def info_modal():
    ui.modal_show(
        ui.modal(
            ui.tags.strong(ui.tags.h3("The Amazon Hydrometeorology Viewer")),
            ui.tags.p(
                "A web-based NetCDF data visualizer"
            ),
            ui.tags.hr(),
            ui.tags.strong(ui.tags.h4("Welcome message,")),
            ui.tags.p(
            """
            This interactive map provides access to estimates of monthly meteorological 
            and hydrological conditions in the Amazon basin, derived from output of 
            a Land Data Assimilation System. The original implementation is described in """,
            ui.tags.a("Recalde et al. (2022).", href = "https://doi.org/10.1175/JHM-D-21-0081.1", target="_blank"), # open url in new tab1

            """ 
            The current, updated system is maintained by Dr. Prakrut Kansara, 
            with visualizations designed by Kris Su. Please direct questions to
            """, ui.tags.a("Ben Zaitchik.", href = "https://eps.jhu.edu/directory/benjamin-zaitchik/", target="_blank"), # open url in new tab2
            style="""
            text-align: justify;
            word-break:break-word;
            hyphens: auto;
            """,
            ),
            #ui.tags.hr(),
            #ui.dataset_information,
            #ui.tags.hr(),
            #ui.missing_note,
            size="l",
            easy_close=True,
            footer=ui.modal_button("Close"),
            #never_hide=False,  # Prevent the modal from being closed by clicking outside
        )
    )

def build_general_info():

    return ui.div(
        ui.tags.p(
                    ui.tags.div('Ensemble forecasting - Instead of making a single forecast of the most ' \
                    'likely weather, a set (or ensemble) of forecasts  is  produced.  This  set  of ' \
                    'forecasts aims to give an indication of ' \
                    'the range of possible future states of ' \
                    'the atmosphere. ')
                ),
        ui.tags.div( # Mermaid diagram
            ui.tags.pre(
            '''
            ---
            config:
            look: handDrawn
            theme: neutral
            ---
            flowchart LR
                Hindcast(Hindcast Data)
                Below(Below Normal)
                Near(Near Normal)
                Above(Above Normal)
                category(Tercile category threshold values)
                Forecast[(Latest initiated forecast)]
                Result>"TERCILE CATEGORY PROBABILITY EXCEEDANCE"]

                Hindcast --Ranking 1 - 33.33 percentile--> Below
                Hindcast --Ranking 33.33 - 66.67 percentile--> Near
                Hindcast --Ranking 66.67 - 100 percentile--> Above

                Below --> category
                Near --> category
                Above --> category

                Forecast --> category

                category --> Result

            ''', class_='mermaid'
            ),
            ui.tags.script("import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';", type="module"),
        )

    )