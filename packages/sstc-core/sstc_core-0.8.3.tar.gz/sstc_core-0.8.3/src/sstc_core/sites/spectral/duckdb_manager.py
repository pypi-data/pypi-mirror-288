import duckdb
import keyring
from sstc_core.sites.spectral import utils, sftp_tools
from sstc_core.sites.spectral.stations import Station, DatabaseError, RecordExistsError


def get_phenocam_table_schema() -> str:
    """
    Returns the SQL schema definition for the Phenocam table.

    This function generates and returns the SQL schema definition as a string for the Phenocam table.
    The schema includes the following columns:
        ```markdown
        - record_id: TEXT (unique identifier)
        - year: INTEGER
        - creation_date: TEXT
        - day_of_year: INTEGER
        - station_acronym: TEXT
        - location_id: TEXT
        - platform_id: TEXT
        - platform_type: TEXT
        - catalog_filepath: TEXT
        - source_filepath: TEXT
        - is_selected: BOOL
        - is_legacy: BOOL
        
        ```

    Returns:
        str: The SQL schema definition for the Phenocam table.
    """
    return """
    record_id TEXT PRIMARY KEY,
    year INTEGER,
    creation_date TEXT,
    day_of_year INTEGER,
    station_acronym TEXT,
    location_id TEXT,
    platform_id TEXT,
    platform_type TEXT,            
    catalog_filepath TEXT,
    source_filepath TEXT, 
    is_selected BOOL,
    is_legacy BOOL    
    """



def _download_files_and_create_records_generator(acronym, location_id, platform_id, platform_type, local_dirpath: str, sftp, sftp_filepaths, split_subdir:str = 'data'):
    """
    Downloads files from an SFTP server and creates record dictionaries for insertion into the database.

    Parameters:
        acronym (str): The station acronym.
        location_id (str): The location ID.
        platform_id (str): The platform ID.
        platform_type (str): The platform type.
        local_dirpath (str): The local directory path to save downloaded files.
        sftp: The SFTP connection object.
        sftp_filepaths (list): List of file paths on the SFTP server to download.
        split_subdir (str): The subdirectory name to split the file path on. Defaults to 'data'.
        
    Yields:
        dict: A dictionary containing record information.
        
    Example:
       ```python
        # Defining variables
        system_name='abisko'
        acronym= 'ANS'
        platform_id= 'P_BTH_1'
        location_id= 'BTH_FOR'
        platform_type: 'PhenoCam'
        
        table_name= 'ANS__BTH_FOR__P_BTH_1'
        db_path = f'/home/aurora02/data/SITES/Spectral/data/catalog/{system_name}_catalog.db'
        local_dirpath = f'/home/aurora02/data/SITES/Spectral/data/catalog/{system_name}/locations/{location_id}/platforms/{platform_type}/{platform_id}'
       
        # Step 1: List files on the SFTP server
        sftp_filepaths = sftp_tools.list_files_sftp(
            hostname=hostname,
            port=port,
            username=username,
            password = password,
            sftp_directory=sftp_directory
        )
        
        # Step 2: Open sftp connection
        sftp, transport = sftp_tools.open_sftp_connection(
            hostname=hostname,
            port=port,
            username=username,
            password = password,
        )
        
        # Step 3: Connect to database
        db = DuckDBManager(db_path=db_path)
        schema = dbm.phenocam_table_schema()
        db.create_table(table_name, schema=schema)
        
        # Step 4: Download files and create records
        
        for record in download_files_and_create_records(
            acronym, 
            location_id, 
            platform_id, 
            platform_type, 
            local_dirpath, 
            sftp, 
            sftp_filepaths, 
            split_subdir='data'):
            
            try:
                db.insert_record(table_name, record)
            except RecordExistsError as e:
                print(e)
            except DatabaseError as e:
                print(e)
                
        sftp.close()
        transport.close()
       
        
       ```
    """
    for remote_filepath in sftp_filepaths:
        # Download the file from the SFTP server
        downloaded_filepath = sftp_tools.download_file(
            sftp,
            remote_filepath=remote_filepath,
            local_dirpath=local_dirpath,
            split_subdir=split_subdir)
        
        # Get creation date and formatted date
        creation_date = utils.get_image_dates(downloaded_filepath)
        formatted_date = creation_date.strftime('%Y-%m-%d %H:%M:%S')
        year = creation_date.year

        try:
            # Create the record dictionary
            record_dict = {
                'record_id': utils.generate_unique_id(formatted_date, acronym, location_id, platform_id),
                'year': year,
                'creation_date': formatted_date,
                'catalog_filepath': downloaded_filepath,
                'source_filepath': remote_filepath,
                'station_acronym': acronym,
                'location_id': location_id,
                'platform_id': platform_id,
                'platform_type': platform_type
            }
            yield record_dict
        except Exception as e:
            print(f"Failed to move file: {e}")


def download_files_and_create_records(platform_dict: dict, db_filepath: str):
    """
    Downloads files from an SFTP server and creates records in the database.

    Parameters:
        platform_dict (dict): A dictionary containing platform information.
        catalog_dict (dict): A dictionary containing catalog information.
        db_filepath (str): The file path to the DuckDB database.
        
    Example:
        ```python
        platform_dict = {
            'system_name': 'abisko',
            'acronym': 'ANS',
            'location_id': 'BTH_FOR',
            'platform_id': 'P_BTH_1',
            'platform_type': 'PhenoCam'
        }
        
        catalog_dict = {
            'sftp_directory': '/abisko/data/PhenoCam/ANS/'
        }
        
        db_filepath = '/home/aurora02/data/SITES/Spectral/data/catalog/abisko_catalog.db'
        
        download_files_and_create_records(platform_dict, catalog_dict, db_filepath)
        ```
    Notes:
        Recommended to be use for first population of the database or
    """
    # SFTP variables
    hostname = keyring.get_password('sftp', 'hostname')
    port = int(keyring.get_password('sftp', 'port'))
    username = keyring.get_password('sftp', 'username')
    password = keyring.get_password('sftp', 'password')
    sftp_directory = f'/{platform_dict["system_name"]}/data/PhenoCam/{platform_dict["legacy_acronym"]}/'
    
    system_name = platform_dict.get('system_name')
    acronym = platform_dict.get('acronym')
    location_id = platform_dict.get('location_id')
    platform_id = platform_dict.get('platform_id')
    platform_type = platform_dict.get('platform_type')
        
    table_name = f'{acronym}__{location_id}__{platform_id}'
    local_dirpath = f'/home/aurora02/data/SITES/Spectral/data/catalog/{system_name}/locations/{location_id}/platforms/{platform_type}/{platform_id}'
    
    # Step 1: List files on the SFTP server
    sftp_filepaths = sftp_tools.list_files_sftp(
        hostname=hostname,
        port=port,
        username=username,
        password=password,
        sftp_directory=sftp_directory
    )
        
    # Step 2: Open SFTP connection
    sftp, transport = sftp_tools.open_sftp_connection(
        hostname=hostname,
        port=port,
        username=username,
        password=password,
    )
        
    # Step 3: Connect to the database
    db = DuckDBManager(db_path=db_filepath)
    schema = get_phenocam_table_schema()
    db.create_table(table_name, schema=schema)
        
    # Step 4: Download files and create records
    for record in _download_files_and_create_records_generator(
        acronym, 
        location_id, 
        platform_id, 
        platform_type, 
        local_dirpath, 
        sftp, 
        sftp_filepaths, 
        split_subdir='data'):
        
        try:
            db.insert_record(table_name, record)
        except RecordExistsError as e:
            print(e)
        except DatabaseError as e:
            print(e)
            
    sftp.close()
    transport.close()
    
    
def get_all_tables(db_path):
    """
    Retrieves all table names from the DuckDB database.

    Parameters:
        db_path (str): The path to the DuckDB database file.

    Returns:
        list: A list of table names present in the database.

    Raises:
        ValueError: If any error occurs during the process.
    """
    try:
        # Connect to DuckDB
        conn = duckdb.connect(database=db_path, read_only=True)

        # Retrieve all table names
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='main';"
        result = conn.execute(query).fetchall()

        # Extract table names from the result
        table_names = [row[0] for row in result]

        return table_names

    except Exception as e:
        raise ValueError(f"An error occurred while retrieving tables from DuckDB: {e}")
    finally:
        # Close the connection
        conn.close()