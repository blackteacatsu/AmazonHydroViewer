# list of variables in the app
list_of_variables = {
    'Rainf_tavg' : 'Precipitation', 
    'Qair_f_tavg' : 'Specific Humidity',
    'Qs_tavg':'Surface Runoff',
    'Evap_tavg':'Evapotranspiration',
    'Tair_f_tavg':'Air Temperature',
    'SoilMoist_inst': 'Soil Moisture',
    'SoilTemp_inst': 'Soil Temperature',
    'Streamflow_tavg': 'Stream Flow'
}

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

# Discrete colorscales for probability data (40-100% in 10% intervals)
# Each bin: 40-50%, 50-60%, 60-70%, 70-80%, 80-90%, 90-100%

# Standard colorscales (for non-temperature variables)
colorscales_discrete = [
    # Reds - Below normal
    [
        [0.0, 'rgb(254, 224, 210)'],     # 40-50%
        [0.1666, 'rgb(254, 224, 210)'],
        [0.1667, 'rgb(252, 187, 161)'],  # 50-60%
        [0.3333, 'rgb(252, 187, 161)'],
        [0.3334, 'rgb(252, 146, 114)'],  # 60-70%
        [0.5, 'rgb(252, 146, 114)'],
        [0.5001, 'rgb(251, 106, 74)'],   # 70-80%
        [0.6666, 'rgb(251, 106, 74)'],
        [0.6667, 'rgb(222, 45, 38)'],    # 80-90%
        [0.8333, 'rgb(222, 45, 38)'],
        [0.8334, 'rgb(165, 15, 21)'],    # 90-100%
        [1.0, 'rgb(165, 15, 21)']
    ],
    # Greys - Near normal
    [
        [0.0, 'rgb(247, 247, 247)'],     # 40-50%
        [0.1666, 'rgb(247, 247, 247)'],
        [0.1667, 'rgb(217, 217, 217)'],  # 50-60%
        [0.3333, 'rgb(217, 217, 217)'],
        [0.3334, 'rgb(189, 189, 189)'],  # 60-70%
        [0.5, 'rgb(189, 189, 189)'],
        [0.5001, 'rgb(150, 150, 150)'],  # 70-80%
        [0.6666, 'rgb(150, 150, 150)'],
        [0.6667, 'rgb(99, 99, 99)'],     # 80-90%
        [0.8333, 'rgb(99, 99, 99)'],
        [0.8334, 'rgb(37, 37, 37)'],     # 90-100%
        [1.0, 'rgb(37, 37, 37)']
    ],
    # Blues - Above normal
    [
        [0.0, 'rgb(239, 243, 255)'],     # 40-50%
        [0.1666, 'rgb(239, 243, 255)'],
        [0.1667, 'rgb(198, 219, 239)'],  # 50-60%
        [0.3333, 'rgb(198, 219, 239)'],
        [0.3334, 'rgb(158, 202, 225)'],  # 60-70%
        [0.5, 'rgb(158, 202, 225)'],
        [0.5001, 'rgb(107, 174, 214)'],  # 70-80%
        [0.6666, 'rgb(107, 174, 214)'],
        [0.6667, 'rgb(49, 130, 189)'],   # 80-90%
        [0.8333, 'rgb(49, 130, 189)'],
        [0.8334, 'rgb(8, 81, 156)'],     # 90-100%
        [1.0, 'rgb(8, 81, 156)']
    ]
]

# Temperature colorscales (inverted: cold=red, warm=blue)
colorscales_discrete_temp = [
    # Blues - Below normal (cold)
    [
        [0.0, 'rgb(239, 243, 255)'],     # 40-50%
        [0.1666, 'rgb(239, 243, 255)'],
        [0.1667, 'rgb(198, 219, 239)'],  # 50-60%
        [0.3333, 'rgb(198, 219, 239)'],
        [0.3334, 'rgb(158, 202, 225)'],  # 60-70%
        [0.5, 'rgb(158, 202, 225)'],
        [0.5001, 'rgb(107, 174, 214)'],  # 70-80%
        [0.6666, 'rgb(107, 174, 214)'],
        [0.6667, 'rgb(49, 130, 189)'],   # 80-90%
        [0.8333, 'rgb(49, 130, 189)'],
        [0.8334, 'rgb(8, 81, 156)'],     # 90-100%
        [1.0, 'rgb(8, 81, 156)']
    ],
    # Greys - Near normal
    [
        [0.0, 'rgb(247, 247, 247)'],     # 40-50%
        [0.1666, 'rgb(247, 247, 247)'],
        [0.1667, 'rgb(217, 217, 217)'],  # 50-60%
        [0.3333, 'rgb(217, 217, 217)'],
        [0.3334, 'rgb(189, 189, 189)'],  # 60-70%
        [0.5, 'rgb(189, 189, 189)'],
        [0.5001, 'rgb(150, 150, 150)'],  # 70-80%
        [0.6666, 'rgb(150, 150, 150)'],
        [0.6667, 'rgb(99, 99, 99)'],     # 80-90%
        [0.8333, 'rgb(99, 99, 99)'],
        [0.8334, 'rgb(37, 37, 37)'],     # 90-100%
        [1.0, 'rgb(37, 37, 37)']
    ],
    # Reds - Above normal (warm)
    [
        [0.0, 'rgb(254, 224, 210)'],     # 40-50%
        [0.1666, 'rgb(254, 224, 210)'],
        [0.1667, 'rgb(252, 187, 161)'],  # 50-60%
        [0.3333, 'rgb(252, 187, 161)'],
        [0.3334, 'rgb(252, 146, 114)'],  # 60-70%
        [0.5, 'rgb(252, 146, 114)'],
        [0.5001, 'rgb(251, 106, 74)'],   # 70-80%
        [0.6666, 'rgb(251, 106, 74)'],
        [0.6667, 'rgb(222, 45, 38)'],    # 80-90%
        [0.8333, 'rgb(222, 45, 38)'],
        [0.8334, 'rgb(165, 15, 21)'],    # 90-100%
        [1.0, 'rgb(165, 15, 21)']
    ]
]

# Legacy continuous colorscale names (for backward compatibility)
colorscales = {
    '0': 'Reds',      # Below normal
    '1':'Greys',      # Near normal
    '2':'Blues'        # Above normal
}

# Inverted colorscales for temperature variables
colorscales_temp = {
    '0': 'Blues',       # Below normal (inverted)
    '1': 'Greys',      # Near normal
    '2': 'Reds'      # Above normal (inverted)
}

# general path to remote backend data
github_data_repo = 'https://raw.githubusercontent.com/Amazon-ARCHive/amazon_hydroviewer_backend/'

probabilistic_data_path = github_data_repo + 'main/get_ldas_probabilistic_output/prob_2024_12_31_tercile_probability_max_'
# pyramid_file = PYRAMID_DIR / f"prob_2024_dec_tercile_probability_max_{variable}_lvl_{profile}_subsampled.pkl"

# general regional averaged forecast data path  @remote location
raw_data_path = github_data_repo + 'refs/heads/main/get_zonal_averages_csv/zonal_stats_pfaf_'

climatology_data_path = github_data_repo + 'refs/heads/main/get_zonal_averages_climatology_csv/zonal_climatology_pfaf_'

# path to geojson file @remote location for visualization
hydrobasins_lev05_url = 'https://raw.githubusercontent.com/blackteacatsu/spring_2024_envs_research_amazon_ldas/main/resources/hybas_sa_lev05_areaofstudy.geojson'

web_app_title = 'Hydrometeorology of The Amazon Basin'

# Pyramid configuration
USE_PYRAMID = True  # Set to False to use original method
PYRAMID_DIR = 'https://raw.githubusercontent.com/Amazon-ARCHive/amazon_hydroviewer_backend/'
PYRAMID_ZOOM_LEVEL = 4  # Which zoom level to use for heatmap (0-5)