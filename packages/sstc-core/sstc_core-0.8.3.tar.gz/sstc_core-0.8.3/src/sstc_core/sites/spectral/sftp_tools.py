import paramiko
import os
import stat
from sstc_core.sites.spectral.utils import extract_two_dirs_and_filename
import keyring
from typing import Dict, Any


def _get_sftp_credentials():
    """
    Retrieves SFTP credentials from the system's keyring.

    This function accesses the system's keyring to fetch the SFTP server credentials securely. The use of a keyring ensures
    that sensitive information, such as the SFTP hostname, port, username, and password, is stored and accessed securely.

    Returns:
        dict: A dictionary containing the SFTP credentials:
            - "hostname": The SFTP server's hostname.
            - "port": The port number used for the SFTP connection.
            - "username": The username for authenticating the SFTP connection.
            - "password": The password for authenticating the SFTP connection.

    Note:
        The credentials retrieved by this function are considered sensitive. Ensure that they are handled securely
        throughout the application's lifecycle. Do not log or expose these credentials in any part of the application
        to avoid potential security risks.

    Example Usage:
        credentials = _get_sftp_credentials()
        print(credentials['hostname'])  # Access hostname securely
    """
    hostname = keyring.get_password('sftp', 'hostname')
    port = int(keyring.get_password('sftp', 'port'))
    username = keyring.get_password('sftp', 'username')
    password = keyring.get_password('sftp', 'password')
    
    return {
        "hostname": hostname,
        "port": port,
        "username": username,
        "password": password
    }


def open_sftp_connection(credentials: Dict[str, Any]):
    """
    Opens an SFTP connection to the specified server using credentials.

    This function establishes an SFTP connection using the provided server details from the credentials
    dictionary and returns the SFTP client and transport objects. It ensures that the connection is properly
    established before returning the objects.

    Parameters:
        credentials (dict): A dictionary containing the SFTP credentials:
            - "hostname": The hostname or IP address of the SFTP server.
            - "port": The port number of the SFTP server.
            - "username": The username for authentication.
            - "password": The password for authentication.

    Returns:
        tuple: A tuple containing the SFTP client and transport objects.

    Raises:
        Exception: If an error occurs while establishing the SFTP connection.

    Example:
        ```python
        credentials = _get_sftp_credentials()
        sftp, transport = open_sftp_connection(credentials)
        # Use the sftp client for file operations
        sftp.close()
        transport.close()
        ```
    """
    try:
        hostname = credentials.get('hostname')
        port = credentials.get('port')
        username = credentials.get('username')
        password = credentials.get('password')

        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp, transport
    except Exception as e:
        raise Exception(f"An error occurred while establishing SFTP connection: {e}")


def list_files_sftp(credentials: Dict[str, Any], sftp_directory: str, extensions=['.jpg', '.jpeg']) -> list:
    """
    Lists files from an SFTP server recursively with specified extensions.

    This function connects to an SFTP server using the provided connection details,
    recursively lists all files starting from the specified directory, and filters the files
    based on the provided extensions.

    Parameters:
        credentials (dict): A dictionary containing the SFTP credentials:
            - "hostname": The hostname or IP address of the SFTP server.
            - "port": The port number of the SFTP server.
            - "username": The username for authentication.
            - "password": The password for authentication.
        sftp_directory (str): The directory on the SFTP server to start listing files from.
        extensions (list): A list of file extensions to filter by. Defaults to ['.jpg', '.jpeg'].

    Returns:
        list: A list of file paths from the SFTP server that match the specified extensions.

    Raises:
        Exception: If an error occurs while connecting to the SFTP server or retrieving files.

    Example:
        ```python
        credentials = _get_sftp_credentials()
        sftp_directory = '/path/to/sftp/directory'
        list_files_sftp(credentials, sftp_directory)
        ['/path/to/sftp/directory/image1.jpg', '/path/to/sftp/directory/subdir/image2.jpeg']
        ```
    """
    try:
        # Open SFTP connection
        sftp, transport = open_sftp_connection(credentials)

        # Function to recursively list files in a directory
        def recursive_list(sftp, directory):
            file_list = []
            for entry in sftp.listdir_attr(directory):
                mode = entry.st_mode
                filename = entry.filename
                filepath = os.path.join(directory, filename)

                if stat.S_ISDIR(mode):  # Directory
                    file_list.extend(recursive_list(sftp, filepath))
                else:  # File
                    if any(filename.lower().endswith(ext) for ext in extensions):
                        file_list.append(filepath)
            return file_list

        # Get all files recursively starting from the specified directory
        all_files = recursive_list(sftp, sftp_directory)

        # Close the SFTP connection
        sftp.close()
        transport.close()
        
        return all_files

    except Exception as e:
        raise Exception(f"An error occurred while listing files from the SFTP server: {e}")


def get_remote_file_size(remote_filepath: str, credentials: dict) -> int:
    """
    Retrieves the size of a remote file on an SFTP server using Paramiko.

    This function connects to an SFTP server using the provided credentials and retrieves the size of the specified
    remote file. The size is returned in bytes. It ensures the proper closing of both SFTP and SSH connections.

    Parameters:
        remote_filepath (str): The path to the remote file on the SFTP server.
        credentials (dict): A dictionary containing the SFTP server credentials with the following keys:
            - 'hostname': The SFTP server's hostname or IP address.
            - 'port': The port number of the SFTP server.
            - 'username': The username to authenticate with the SFTP server.
            - 'password': The password to authenticate with the SFTP server.

    Returns:
        int: The size of the file in bytes.

    Raises:
        Exception: If there is an error connecting to the SFTP server or retrieving the file size.

    Example:
        ```python
        credentials = {
            'hostname': 'example.com',
            'port': 22,
            'username': 'your_username',
            'password': 'your_password'
        }
        remote_filepath = '/remote/path/to/file.txt'
        file_size = get_remote_file_size(remote_filepath, credentials)
        print(f"The size of the remote file is: {file_size} bytes")
        ```
    """
    # Initialize the SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SFTP server
        ssh.connect(
            hostname=credentials['hostname'],
            port=credentials['port'],
            username=credentials['username'],
            password=credentials['password']
        )
        sftp = ssh.open_sftp()

        # Get the file attributes and retrieve the file size
        file_attributes = sftp.stat(remote_filepath)
        file_size = file_attributes.st_size

        # Close the SFTP connection
        sftp.close()

        return file_size
    finally:
        # Close the SSH connection
        ssh.close()

    
def get_local_filepath(local_dirpath: str, remote_filepath: str, split_subdir: str = 'data') -> str:
    """
    Constructs the local file path for a file from a remote SFTP server based on a specific directory structure.

    This function takes a remote file path and reconstructs the corresponding local file path using the base
    local directory (`local_dirpath`). It uses a specified subdirectory name (`split_subdir`) to determine the
    starting point for constructing the local path from the remote file path structure.

    Parameters:
        local_dirpath (str): The base directory path where the files are stored locally.
        remote_filepath (str): The full path of the file on the remote SFTP server.
        split_subdir (str, optional): The subdirectory in the remote path from which to start building the local path.
                                      Default is 'data'.

    Returns:
        str: The constructed local file path.
    """
    # Split the remote file path into components
    parts = remote_filepath.split('/')
    filename = parts[-1]

    # Find the index of the split_subdir in the parts
    if split_subdir in parts:
        split_index = parts.index(split_subdir)
        remote_subdir = os.path.join(*parts[split_index:])
    else:
        remote_subdir = ""
        
    # Construct the local file path using the structure from the split_subdir to the filename
    local_filepath = os.path.join(local_dirpath, remote_subdir)
    return local_filepath


def is_file_downloaded_locally(local_dirpath: str, remote_filepath: str, split_subdir: str = 'data') -> bool:
    """
    Checks if a file from a remote SFTP server is downloaded locally, based on a specific directory structure.

    This function determines if a file specified by a remote filepath is present in the local directory.
    It uses a specified subdirectory name (`split_subdir`) to construct the local path relative to the base
    local directory (`local_dirpath`). The check is performed by comparing the reconstructed local path
    with the actual file system.

    Parameters:
        local_dirpath (str): The base directory path where the files are expected to be downloaded locally.
        remote_filepath (str): The full path of the file on the remote SFTP server.
        split_subdir (str, optional): The subdirectory in the remote path to start building the local path from.
                                      Default is 'data'.

    Returns:
        bool: True if the file exists locally, False otherwise.
    """
    
    local_filepath = get_local_filepath(local_dirpath=local_dirpath,remote_filepath=remote_filepath,split_subdir=split_subdir)
    if os.path.exists(local_filepath):
        return True 
    else:
        return False
        

def download_file(sftp: paramiko.SFTPClient, remote_filepath: str, local_dirpath: str, split_subdir: str = 'data', skip_download: bool = True) -> str:
    """
    Downloads a file from the SFTP server and ensures that the download is complete by verifying the file size.

    This function downloads a file from the specified remote path on the SFTP server to the specified local directory path.
    The filename is extracted from the remote path and used to construct the local file path. After downloading, it verifies
    that the file size matches the size on the SFTP server. If the sizes do not match, it raises a ValueError indicating a file size mismatch.

    Parameters:
        sftp (paramiko.SFTPClient): An active SFTP client connection.
        remote_filepath (str): The path to the remote file on the SFTP server.
        local_dirpath (str): The path to the local directory where the download will be saved.
        split_subdir (str): The subdirectory name to split the file path on. Defaults to 'data'.
        skip_download (bool): Whether to skip downloading the file if it already exists locally. Defaults to True.

    Returns:
        str: The path to the local file if the download was successful.

    Raises:
        ValueError: If the file size of the downloaded file does not match the file size on the SFTP server.
        Exception: If any other error occurs during the file download process.

    Example:
        ```python    
        credentials = _get_sftp_credentials()
        remote_filepath = '/remote/path/to/data/subdir1/file1.jpg'
        local_dirpath = '/local/path/to/directory'
        sftp, transport = open_sftp_connection(credentials)
        download_file(sftp, remote_filepath, local_dirpath, 'data')
        sftp.close()
        transport.close()
        ```
    """
    try:
        # Construct the local file path based on the remote file path
        local_filepath = get_local_filepath(local_dirpath=local_dirpath, remote_filepath=remote_filepath, split_subdir=split_subdir)

        # Check if the file already exists and skip download if specified
        if skip_download and os.path.exists(local_filepath):
            print(f"File {local_filepath} already exists. Skipping download.")
            return local_filepath

        # Ensure the local directory exists
        os.makedirs(os.path.dirname(local_filepath), exist_ok=True)

        # Download the file from the SFTP server
        sftp.get(remote_filepath, local_filepath)

        # Verify the file size
        remote_file_size = sftp.stat(remote_filepath).st_size
        local_file_size = os.path.getsize(local_filepath)

        if remote_file_size != local_file_size:
            raise ValueError(f"Download failed for {remote_filepath}: file size mismatch. "
                             f"Remote size: {remote_file_size}, Local size: {local_file_size}")

        # Return the local file path if the download was successful
        return local_filepath

    except Exception as e:
        raise Exception(f"An error occurred while downloading {remote_filepath}: {e}")
    

def get_new_files_to_download(local_dirpath: str, sftp_filepaths: list, split_subdir: str = 'data') -> list:
    """
    Identifies files that need to be downloaded from an SFTP server by comparing the list of remote filepaths
    with the files already present in the local directory.

    This function checks if each file in the list of remote filepaths (`sftp_filepaths`) has already been downloaded
    to the specified local directory (`local_dirpath`). It uses a subdirectory structure (`split_subdir`) to organize
    the files locally. If a file is not found locally, it is added to the list of files to be downloaded.

    Parameters:
        local_dirpath (str): The base directory path where the files are stored locally.
        sftp_filepaths (list): A list of filepaths on the SFTP server to check against the local directory.
        split_subdir (str, optional): The subdirectory name to split the file path on. Defaults to 'data'.

    Returns:
        list: A list of filepaths that are not present locally and need to be downloaded.

    Example:
        ```python
        local_dirpath = '/local/path/to/directory'
        sftp_filepaths = [
            '/remote/path/to/data/file1.jpg',
            '/remote/path/to/data/file2.jpg'
        ]
        files_to_download = get_new_files_to_download(local_dirpath, sftp_filepaths)
        print(files_to_download)
        # Output: ['/remote/path/to/data/file1.jpg', '/remote/path/to/data/file2.jpg'] if these files are not locally available
        ```
    """
    files_to_download = []
    
    for remote_filepath in sftp_filepaths:
        if not is_file_downloaded_locally(
            local_dirpath=local_dirpath,
            remote_filepath=remote_filepath,
            split_subdir=split_subdir     
        ):
            files_to_download.append(remote_filepath)
    
    return files_to_download