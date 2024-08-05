from ..io_tools import load_yaml
from pathlib import Path

stations_dirpath = Path(__file__).parent
spectral_dirpath = Path(stations_dirpath).parent
config_dirpath = spectral_dirpath / "config"
catalog_db_filepath = config_dirpath / "catalog_db_filepaths.yaml"

meta = {
    "version": '2024_v0.3',
    "station_acronym": "ANS",
    "long_station_name": "Abisko Scientific Research Station",
    "is_active": True,
    "station_name": "Abisko",
    "normalized_station_name": "abisko",    
    "locations_filepath": config_dirpath / 'locations' / 'locations_abisko.yaml',
    "platforms_filepath": config_dirpath / 'platforms' / 'platforms_abisko.yaml',
    "phenocam_quality_weights_filepath": config_dirpath / "phenocam_quality_weights.yaml",    
    'geolocation':{
        'point':{
            'epsg:4326': {'latitude_dd': None, 'longitude_dd': None}, 
            'epsg:3006': {'x_coord': None, 'y_coord': None}},
    }
    
    }

def load_configurations():
    """
    Loads configurations for the Abisko station from YAML files.

    Returns:
      tuple: A tuple containing locations and platforms configuration data.
    """
    # Loading station locations config
    locations = load_yaml(meta["locations_filepath"])

    # Loading station platforms config
    platforms = load_yaml(meta["platforms_filepath"])

    return locations, platforms


locations, platforms = load_configurations()


    

