import os
from datetime import datetime, timedelta
from PIL import Image
from PIL.ExifTags import TAGS
from shutil import copy2
from typing import Dict, Any
import unicodedata
import hashlib
import base64


def generate_unique_id(data: dict, variable_names: list = None) -> str:
    """
    Generates a unique global identifier based on the provided variable names from the data dictionary.

    Parameters:
        data (dict): A dictionary containing the data fields.
        variable_names (list, optional): A list of variable names to include in the unique identifier. 
                                         Defaults to ['creation_date', 'station_acronym', 'location_id', 'platform_id'].

    Returns:
        str: A short unique global identifier.
    """
    if variable_names is None:
        variable_names = ['creation_date', 'station_acronym', 'location_id', 'platform_id']

    # Concatenate the specified fields from the data dictionary to form a unique string
    unique_string = "_".join(str(data[var]) for var in variable_names if var in data)
    
    # Generate the SHA-256 hash of the unique string
    hash_object = hashlib.sha256(unique_string.encode())
    hash_digest = hash_object.digest()
    
    # Take the first 12 bytes of the hash and encode them in Base64
    short_hash = base64.urlsafe_b64encode(hash_digest[:12]).decode('utf-8').rstrip('=')
    
    return short_hash

def day_of_year_to_month_day(year, day_of_year):
    # Calculate the date corresponding to the day of year
    date = datetime(year, 1, 1) + timedelta(days=day_of_year - 1)
    # Format the date as "MMM DD"
    return date.strftime('%b %d')

def extract_year(creation_date:str):
    """
    Extracts the year from the creation date.

    Parameters:
        creation_date (str): The creation date in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
        int: The year extracted from the creation date.
    """
    date_obj = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
    return date_obj.year


def get_image_dates(filepath:str)->str:
    """
    Extracts the creation date from an image file's EXIF data.

    Parameters:
        filepath (str): The path to the image file.

    Returns:
        datetime: The creation date of the image if found, otherwise None.

    Raises:
        Exception: If an error occurs during the extraction process, it will print an error message.
    """
    try:
        image = Image.open(filepath)
        exif_data = image._getexif()

        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'DateTimeOriginal':
                    creation_date = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                    return creation_date
    except Exception as e:
        print(f"An error occurred with file {filepath}: {e}")
    return None


def list_image_files(dirpath:str, extensions:list = ['.jpg', '.jpeg']):
    """
    Lists all image files in a directory and its subdirectories with specified extensions.

    Parameters:
        dirpath (str): The root directory to search for image files.
        extensions (list): A list of file extensions to include in the search. Defaults to ['.jpg', '.JPEG', '.jpeg', '.JPG'].

    Returns:
        list: A list of file paths that match the specified extensions.
    """
    file_paths = []
    for root, _, files in os.walk(dirpath):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                file_paths.append(os.path.join(root, file))
    return file_paths


def group_images_by_date(filepaths: list):
    """
    Groups image files by their creation dates.

    This function takes a list of image file paths, extracts the creation date for each image,
    and groups the images by these dates. The grouped images are stored in a dictionary where 
    the keys are formatted creation dates and the values are lists of file paths that correspond
    to those dates.

    Parameters:
        filepaths (list): A list of file paths to the image files.

    Returns:
        dict: A dictionary where keys are formatted creation dates (as strings) and values are lists 
          of file paths that have those creation dates.

    Example:
        ```python    
        filepaths = ['/path/to/image1.jpg', '/path/to/image2.jpg']
        group_images_by_date(filepaths)
        {
            '2023-01-01 12:00:00': ['/path/to/image1.jpg'],
            '2023-01-02 13:00:00': ['/path/to/image2.jpg']
        }
        ```
    """
    date_dict = {}

    for filepath in filepaths:
        creation_date = get_image_dates(filepath)
        if creation_date:
            formatted_date = creation_date.strftime('%Y-%m-%d %H:%M:%S')
            if formatted_date not in date_dict:
                date_dict[formatted_date] = []
            date_dict[formatted_date].append(filepath)

    return date_dict


def filter_keys_with_multiple_files(image_date_dict:dict):
    """
    Filters and returns the keys from the image_date_dict that have multiple file paths.

    This function is used to detect duplicates by identifying keys (formatted creation dates)
    that have more than one file path associated with them in the provided dictionary.

    Parameters:
        image_date_dict (dict): A dictionary where keys are formatted creation dates (as strings) 
                            and values are lists of file paths that correspond to those dates.

    Returns:
        list: A list of keys (formatted creation dates) that have multiple file paths, indicating duplicates.

    Example:
        ```python
        image_date_dict = {
             '2023-01-01 12:00:00': ['/path/to/image1.jpg', '/path/to/image1_duplicate.jpg'],
             '2023-01-02 13:00:00': ['/path/to/image2.jpg']
        }
        filter_keys_with_multiple_files(image_date_dict)
        ['2023-01-01 12:00:00']
        ```
    """
    return [key for key, value in image_date_dict.items() if len(value) > 1]


def extract_two_dirs_and_filename(filepaths:list):
    """
    Extracts the last two subdirectories and the filename from a list of file paths.

    This function processes a list of file paths, extracts the last two subdirectories and 
    the filename from each path, and returns a dictionary where the keys are tuples 
    containing the two subdirectories and the filename (or fewer components if not enough 
    subdirectories are present), and the values are the full file paths.

    Parameters:
        filepaths (list): A list of file paths to process.

    Returns:
        dict: A dictionary where keys are tuples of (subdir_1, subdir_2, filename) or fewer
          components, and values are the corresponding full file paths.

    Example:
        ```python    
        filepaths = [
             '/path/to/subdir1/file1.jpg',
             '/another/path/to/subdir2/file2.jpg',
             '/file3.jpg'
         ]
        extract_two_dirs_and_filename(filepaths)
        {
            ('to', 'subdir1', 'file1.jpg'): '/path/to/subdir1/file1.jpg',
            ('to', 'subdir2', 'file2.jpg'): '/another/path/to/subdir2/file2.jpg',
            ('file3.jpg',): '/file3.jpg'
        }
        ```
    """
    extracted = {}
    for filepath in filepaths:
        parts = filepath.split(os.sep)
        if len(parts) >= 3:
            key = (parts[-3], parts[-2], parts[-1])
        elif len(parts) == 2:
            key = (parts[-2], parts[-1])
        elif len(parts) == 1:
            key = (parts[-1],)
        else:
            continue  # Skip empty or invalid file paths
        extracted[key] = filepath
    return extracted


def get_day_of_year(formatted_date: str) -> str:
    """
    Calculates the day of the year from a formatted date string and returns it as a string with leading zeros.

    Parameters:
        formatted_date (str): The date string in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        str: The day of the year corresponding to the given date, formatted as a three-digit string with leading zeros.
    """
    date_obj = datetime.strptime(formatted_date, '%Y-%m-%d %H:%M:%S')
    day_of_year = date_obj.timetuple().tm_yday
    return f"{day_of_year:03d}"


def phenocam_save_selected_images(filepaths_by_year_and_day: Dict[int, Dict[int, Dict[str, Dict[str, Any]]]], destination_dir: str):
    """
    Saves images with `is_selected` set to True to the specified destination directory.

    Parameters:
        filepaths_by_year_and_day (Dict[int, Dict[int, Dict[str, Dict[str, Any]]]]): Nested dictionary containing the data.
        destination_dir (str): The directory where the images will be saved.

    Returns:
        None
    """
    # Ensure the destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Iterate through the data structure
    for year, days in filepaths_by_year_and_day.items():
        for day_of_year, records in days.items():
            for L0_name, data in records.items():
                if data.get('is_selected', False):
                    src_filepath = data['catalog_filepath']
                    if os.path.exists(src_filepath):
                        # Define the destination file path
                        filename = f"{L0_name}_{os.path.basename(src_filepath)}"
                        dest_filepath = os.path.join(destination_dir, filename)
                        
                        # Copy the file to the destination directory
                        copy2(src_filepath, dest_filepath)
                        print(f"Saved: {dest_filepath}")
                    else:
                        print(f"File not found: {src_filepath}")
                        
                        
def normalize_string(input_string: str) -> str:
    """
    Normalizes a string by converting it to lowercase and replacing accented or non-English
    characters with their corresponding English characters. Specially handles Nordic characters.

    Parameters:
        input_string (str): The string to normalize.

    Returns:
        str: The normalized string with all characters in lowercase and accented characters replaced.
    """
    # Decompose the unicode string into its components (base characters and diacritics)
    normalized = unicodedata.normalize('NFKD', input_string)

    # Encode the decomposed string into ASCII, ignoring non-ASCII characters (diacritics)
    ascii_bytes = normalized.encode('ASCII', 'ignore')

    # Decode the bytes back into a string
    ascii_string = ascii_bytes.decode('ASCII')

    # Convert to lowercase
    lower_string = ascii_string.lower()

    return lower_string


def is_within_time_window(formatted_date: str, start_time: str = "10:00:00", end_time: str = "14:00:00") -> bool:
    """
    Checks if the given date and time fall within the specified time window.

    Parameters:
        formatted_date (str): The date and time in the format '%Y-%m-%d %H:%M:%S'.
        start_time (str): The start of the time window in 'HH:MM:SS' format. Default is "10:00:00".
        end_time (str): The end of the time window in 'HH:MM:SS' format. Default is "14:00:00".

    Returns:
        bool: True if the time part of the formatted_date is within the time window, False otherwise.
    """
    # Convert the start and end times to time objects
    start_time_obj = datetime.strptime(start_time, '%H:%M:%S').time()
    end_time_obj = datetime.strptime(end_time, '%H:%M:%S').time()

    # Convert the formatted date to a datetime object and extract the time part
    date_obj = datetime.strptime(formatted_date, '%Y-%m-%d %H:%M:%S')
    creation_time = date_obj.time()

    # Check if the creation_time is within the time window
    return start_time_obj <= creation_time <= end_time_obj


def extract_keys_with_prefix(input_dict, starts_with='flag_'):
    """
    Extracts keys from the input dictionary that start with the specified prefix.

    Args:
        input_dict (dict): The dictionary to filter.
        starts_with (str): The prefix to filter keys by. Default is 'flag_'.

    Returns:
        dict: A new dictionary with only the keys starting with the specified prefix and their corresponding values.
    """
    return {key: value for key, value in input_dict.items() if key.startswith(starts_with)}

def set_all_values_to_false(input_dict:dict)->dict:
    """
    Sets all the values of the given dictionary to False.

    Args:
        input_dict (dict): The dictionary whose values will be set to False.

    Returns:
        dict: The dictionary with all values set to False.
    """
    return {key: False for key, value in input_dict.items()}

def have_values_changed(dict1, dict2):
    """
    Compares two dictionaries and returns a dictionary with the keys and new state
    values that have changed. Returns None if no values have changed.

    Args:
        dict1 (dict): The first dictionary representing the original state.
        dict2 (dict): The second dictionary representing the new state.

    Returns:
        dict or None: A dictionary with changed keys and their new values, or None if no changes.
    """
    changed_values = {}

    # Iterate over the keys in the dictionaries and compare values
    for key in dict1:
        if key in dict2 and dict1[key] != dict2[key]:
            changed_values[key] = dict2[key]

    # Return the dictionary with changed values if any, otherwise return None
    return changed_values if changed_values else None
