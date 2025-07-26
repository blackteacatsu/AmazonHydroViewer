from pathlib import Path

# list of variables in the app
list_of_variables = {
    'Rainf_tavg' : 'Average precipitation', 
    'Qair_f_tavg' : 'Specific humidity',
    'Qs_tavg':'Surface runoff',
    'Evap_tavg':'Evapotranspiration',
    'Tair_f_tavg':'Avg. air temperature',
    'SoilMoist_inst': 'Soil moisture',
    'SoilTemp_inst': 'Soil temperature',
    'Streamflow_tavg': 'Stream flow'
}

## Global variables
surface_variable_short = [
    'Rainf_tavg', 
    'Qair_f_tavg',
    'Qs_tavg',
    'Evap_tavg',
    'Tair_f_tavg',
    'SoilMoist_inst', 
    'SoilTemp_inst'
]

surface_variable_unit = {
    'Rainf_tavg':'mm/day', 
    'Qair_f_tavg':'g/kg', 
    'Qs_tavg':'mm/day', 
    'Evap_tavg':'mm/day',
    'Tair_f_tavg':'degree Celsius',
    'SoilMoist_inst':'m^3 m-3', 
    'SoilTemp_inst':'degree Celsius',
    'Streamflow_tavg': ''
}

# list of profile indices and corresponding meaning
list_of_profiles = {
    0: '0-10cm', 
    1: '10-40cm', 
    2: '40-100cm', 
    3: '100-200cm'
}

# list of prob data category
list_of_pcate = {
    0:'Below noraml',
    1:'Near normal',
    2:'Above normal'
}

# List of Plotly colorscales (add more if needed)
colorscales = [
    "Blues", 
    'oranges', 
    "Reds"
]

"""
    'Viridis', 'Cividis', 'Plasma', 'Magma', 'Inferno', 
    'Turbo', 'YlGnBu', 'RdBu', 'Picnic', 'Jet'
"""

# get external style sheet
css_file_path = Path(__file__).parent / "styles.css"

github_data_repo = 'https://raw.githubusercontent.com/Amazon-ARCHive/amazon_hydroviewer_backend/main/'

probabilistic_data_path = github_data_repo + 'get_ldas_probabilistics_output/prob_2024_12_31_tercile_probability_max_'

deterministic_data_path = github_data_repo + 'get_ldas_probabilistics_output'

hydrobasins_lev05_url = 'https://raw.githubusercontent.com/blackteacatsu/spring_2024_envs_research_amazon_ldas/main/resources/hybas_sa_lev05_areaofstudy.geojson'

surface_ensemble_members_path = Path(__file__).parent / 'data' / 'get_ldas_deterministic_output' / 'monthly_ldas_surfacemodel_2024_jul30.nc'

routing_ensemble_members_path = Path(__file__).parent / 'data' / 'get_ldas_deterministic_output' / 'monthly_ldas_routing_2024_jul30.nc'


web_app_title = 'Hydrometeorology of The Amazon Basin'

documentation_site_url = 'https://blackteacatsu.github.io/dokkuments/'