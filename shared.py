# list of variables in the app
CLIM_VAR_META = VARIABLE_META = {
    "Rainf_tavg": {
        "long_name": "Precipitation",
        "unit": "mm/day",
    },
    "Qair_f_tavg": {
        "long_name": "Specific Humidity",
        "unit": "g/kg",
    },
    "Qs_tavg": {
        "long_name": "Surface Runoff",
        "unit": "mm/day",
    },
    "Evap_tavg": {
        "long_name": "Evapotranspiration",
        "unit": "mm/day",
    },
    "Tair_f_tavg": {
        "long_name": "Air Temperature",
        "unit": "degree Celsius",
    },
    "SoilMoist_inst": {
        "long_name": "Soil Moisture",
        "unit": "m^3 m-3",
    },
    "SoilTemp_inst": {
        "long_name": "Soil Temperature",
        "unit": "degree Celsius",
    },
    "Streamflow_tavg": {
        "long_name": "Stream Flow",
        "unit": "m^3/sec",
    },
}

# list of profile indices and corresponding meaning
SOIL_VAR_PROFILE = {
    0: '0-10cm', 
    1: '10-40cm', 
    2: '40-100cm', 
    3: '100-200cm'
}

# list of prob data category
FORECAST_PCATE = {
    0:'Below normal',
    1:'Near normal',
    2:'Above normal'
}

# Legacy continuous colorscale names (for backward compatibility)
# colorscales = {
#     '0': 'Reds',      # Below normal
#     '1':'Greys',      # Near normal
#     '2':'Blues'        # Above normal
# }

# # Inverted colorscales for temperature variables
# colorscales_temp = {
#     '0': 'Blues',       # Below normal (inverted)
#     '1': 'Greys',      # Near normal
#     '2': 'Reds'      # Above normal (inverted)
# }

# general path to remote backend data
BACKEND_DIR = 'https://raw.githubusercontent.com/Amazon-ARCHive/amazon_hydroviewer_backend/refs/heads/main/'

# probabilistic_data_path = REMOTE_REPO + 'get_ldas_probabilistic_output/prob_2024_12_31_tercile_probability_max_'
# pyramid_file = PYRAMID_DIR / f"prob_2024_dec_tercile_probability_max_{variable}_lvl_{profile}_subsampled.pkl"

# general regional averaged forecast data path  @remote location
ZONAL_FORECAST_PATH = BACKEND_DIR + 'get_zonal_averages_forecast_csv/zonal_forecast_pfaf_'

ZONAL_CLIM_PATH = BACKEND_DIR + 'get_zonal_averages_climatology_csv/zonal_climatology_pfaf_'

# path to geojson file @remote location for visualization
hydrobasins_lev05_url = 'https://raw.githubusercontent.com/blackteacatsu/spring_2024_envs_research_amazon_ldas/main/resources/hybas_sa_lev05_areaofstudy.geojson'

# Pyramid configuration
USE_PYRAMID = True  # Set to False to use original method
PYRAMID_DIR = 'https://raw.githubusercontent.com/Amazon-ARCHive/amazon_hydroviewer_backend/'
PYRAMID_ZOOM_LEVEL = 4  # Which zoom level to use for heatmap (0-5)