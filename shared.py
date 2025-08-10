# list of variables in the app
list_of_variables = {
    'Rainf_tavg' : 'average precipitation', 
    'Qair_f_tavg' : 'specific humidity',
    'Qs_tavg':'surface runoff',
    'Evap_tavg':'evapotranspiration',
    'Tair_f_tavg':'avg. air temperature',
    'SoilMoist_inst': 'soil moisture',
    'SoilTemp_inst': 'soil temperature',
    #'Streamflow_tavg': 'stream flow'
}

"""# Global variables
surface_variable_short = [
    'Rainf_tavg', 
    'Qair_f_tavg',
    'Qs_tavg',
    'Evap_tavg',
    'Tair_f_tavg',
    'SoilMoist_inst', 
    'SoilTemp_inst'
]"""

# list of surface variable units
surface_variable_unit = {
    'Rainf_tavg':'mm/day', 
    'Qair_f_tavg':'g/kg', 
    'Qs_tavg':'mm/day', 
    'Evap_tavg':'mm/day',
    'Tair_f_tavg':'degree Celsius',
    'SoilMoist_inst':'m^3 m-3', 
    'SoilTemp_inst':'degree Celsius',
    #'Streamflow_tavg': ''
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
    0:'Below normal',
    1:'Near normal',
    2:'Above normal'
}

# List of Plotly colorscales (add more if needed)
colorscales = [
    "Blues", 
    'Oranges', 
    "Reds"
]

"""
    'Viridis', 'Cividis', 'Plasma', 'Magma', 'Inferno', 
    'Turbo', 'YlGnBu', 'RdBu', 'Picnic', 'Jet'
"""

# get external style sheet
github_data_repo = 'https://raw.githubusercontent.com/Amazon-ARCHive/amazon_hydroviewer_backend/'

probabilistic_data_path = github_data_repo + 'main/get_ldas_probabilistics_output/prob_2024_12_31_tercile_probability_max_'

deterministic_data_path = github_data_repo + 'main/get_ldas_probabilistics_output'

raw_data_path = github_data_repo + 'refs/heads/main/get_zonal_averages_csv/zonal_stats_pfaf_'


hydrobasins_lev05_url = 'https://raw.githubusercontent.com/blackteacatsu/spring_2024_envs_research_amazon_ldas/main/resources/hybas_sa_lev05_areaofstudy.geojson'


web_app_title = 'Hydrometeorology of The Amazon Basin'

documentation_site_url = 'https://blackteacatsu.github.io/dokkuments/'