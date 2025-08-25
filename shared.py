# list of variables in the app (short & long names)
list_of_variables = {
    'Rainf_tavg' : 'Average Precipitation', 
    'Qair_f_tavg' : 'Specific Humidity',
    'Qs_tavg':'Surface Runoff',
    'Evap_tavg':'Evapotranspiration',
    'Tair_f_tavg':'Avg. Air Temperature',
    'SoilMoist_inst': 'Soil Moisture',
    'SoilTemp_inst': 'Soil Temperature',
    #'Streamflow_tavg': 'Stream Flow'
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
all_variable_units = {
    'Rainf_tavg':'mm/day', 
    'Qair_f_tavg':'g/kg', 
    'Qs_tavg':'mm/day', 
    'Evap_tavg':'mm/day',
    'Tair_f_tavg':'degree Celsius',
    'SoilMoist_inst':'m^3 m-3', 
    'SoilTemp_inst':'degree Celsius',
    'Streamflow_tavg': 'm^3/sec'
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

# general path to remote backend data
github_data_repo = 'https://raw.githubusercontent.com/Amazon-ARCHive/amazon_hydroviewer_backend/'

# general probabilistic data path  @remote location
probabilistic_data_path = github_data_repo + 'main/get_ldas_probabilistics_output/prob_2024_12_31_tercile_probability_max_'

# general regional averaged forecast data path  @remote location
raw_data_path = github_data_repo + 'refs/heads/main/get_zonal_averages_csv/zonal_stats_pfaf_'

# general regional climatology data path  @remote location
climatology_data_path = github_data_repo + 'refs/heads/main/get_zonal_averages_climatology_csv/zonal_climatology_pfaf_'

# path to geojson file @remote location for visualization
hydrobasins_lev05_url = 'https://raw.githubusercontent.com/blackteacatsu/spring_2024_envs_research_amazon_ldas/main/resources/hybas_sa_lev05_areaofstudy.geojson'

web_app_title = 'Hydrometeorology of The Amazon Basin'