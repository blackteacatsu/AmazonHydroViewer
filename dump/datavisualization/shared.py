from pathlib import Path

# list of variables in the app
list_of_variables = {'Rainf_tavg' : 'Average precipitation', 
                     'Qair_f_tavg' : 'Specific humidity',
                     'Qs_tavg':'Surface runoff',
                     'Evap_tavg':'Evapotranspiration',
                     'SoilMoist_inst': 'Soil moisture',
                     'SoilTemp_inst': 'Soil temperature',
                     'Streamflow_tavg': 'Stream flow'}

# list of profile indices and corresponding meaning
list_of_profiles = {0: '0-10cm', 
                    1: '10-40cm', 
                    2: '40-100cm', 
                    3: '100-200cm'}

# get external style sheet
css_file_path = Path(__file__).parent / "styles.css"

hydrobasins_lev05_url = 'https://raw.githubusercontent.com/blackteacatsu/spring_2024_envs_research_amazon_ldas/main/resources/hybas_sa_lev05_areaofstudy.geojson'

surface_ensemble_members_path = Path(__file__).parent / 'data' / 'monthly_ldas_surfacemodel_2024_jul30.nc'

routing_ensemble_members_path = Path(__file__).parent / 'data' / 'monthly_ldas_routing_2024_jul30.nc'

web_app_title = 'Hydrometeorology of The Amazon Basin'

documentation_site_url = 'https://blackteacatsu.github.io/dokkuments/'