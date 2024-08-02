import urllib.request
import re
import os
import argparse
import sys
import time
import logging
import hashlib
from packaging import version
from datetime import datetime

# Set up logging to track events
logging.basicConfig(filename='log_update.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL paths for retrieving version and program data
REMOTE_VERSION_URL = 'http://localhost:8000/application.txt'
REMOTE_PROGRAM_URL = 'http://localhost:8000/hello.py'
REMOTE_CHECKSUM_URL = 'http://localhost:8000/checksum.txt'
LOCAL_PROGRAM_FILE = 'hello.py'
LOCAL_VERSION_FILE = 'application.txt'

def fetch_file(url):
    """
    Fetch the content of a file from a given URL.

    Args:
        url (str): The URL from which to fetch the file.

    Returns:
        str: The content of the file, or None if an error occurs.
    """
    try:
        return urllib.request.urlopen(url).read().decode('utf-8').strip()
    except Exception as e:
        logging.error(f"Error fetching file from {url}: {e}")
        return None

def extract_version(text):
    """
    Extract version information from a given text.

    Args:
        text (str): The text containing version information.

    Returns:
        tuple: A tuple containing the version number and any additional prefix information.
    """
    match = re.search(r'version\s+(\d+\.\d+\.\d+)([-\w]*)', text, re.IGNORECASE)
    return (match.group(1), match.group(2).strip()) if match else (None, None)

def calculate_checksum(file_path):
    """
    Calculate the SHA256 checksum of a file.

    Args:
        file_path (str): The path to the file for which to calculate the checksum.

    Returns:
        str: The calculated checksum as a hexadecimal string.
    """
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def validate_checksum(local_path, expected_checksum):
    """
    Validate the checksum of a downloaded file.

    Args:
        local_path (str): The path to the local file.
        expected_checksum (str): The expected checksum value.

    Returns:
        bool: True if the calculated checksum matches the expected value, False otherwise.
    """
    return calculate_checksum(local_path) == expected_checksum

def download_file(url, path):
    """
    Download a file from a specified URL to a local path.

    Args:
        url (str): The URL from which to download the file.
        path (str): The local file path where the downloaded file should be saved.

    Returns:
        None
    """
    try:
        urllib.request.urlretrieve(url, path)
        logging.info(f"Downloaded {url} to {path}")
    except Exception as e:
        logging.error(f"Error downloading file from {url} to {path}: {e}")

def compare_versions(r_ver, r_pre, l_ver, l_pre):
    """
    Compare remote and local versions to determine if an update is needed.

    Args:
        r_ver (str): Remote version number.
        r_pre (str): Remote version prefix.
        l_ver (str): Local version number.
        l_pre (str): Local version prefix.

    Returns:
        bool: True if an update is needed, False otherwise.
    """
    return version.parse(r_ver) > version.parse(l_ver) or (r_ver == l_ver and r_pre != l_pre)

def clear_console():
    """
    Clear the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def show_progress_bar():
    """
    Display a simple progress bar for user feedback during updates.
    """
    sys.stdout.write('Updating')
    for _ in range(3):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write('\n')
    sys.stdout.flush()

def check_for_update():
    """
    Check if a new version of the program is available.

    Returns:
        tuple: A tuple containing a boolean indicating if an update is available,
               and the remote version and prefix.
    """
    remote_text = fetch_file(REMOTE_VERSION_URL)
    if not remote_text:
        exit(1)
    
    r_version, r_prefix = extract_version(remote_text)
    l_version, l_prefix = (extract_version(open(LOCAL_VERSION_FILE).read()) if os.path.exists(LOCAL_VERSION_FILE) else (None, None))

    update_needed = compare_versions(r_version, r_prefix, l_version, l_prefix)
    if update_needed:
        print(f"New version available: {r_version}{' ' + r_prefix if r_prefix else ''}")
    return update_needed, r_version, r_prefix

def perform_update():
    """
    Perform the update process, including downloading the new version,
    creating a backup of the current version, and verifying the download.
    """
    # clear_console()
    logging.info('Starting update process.')
    try:
        # Create backup of the current program file if it exists
        if os.path.exists(LOCAL_PROGRAM_FILE):
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            backup_file = f"backup_{timestamp}_{LOCAL_PROGRAM_FILE}"
            os.rename(LOCAL_PROGRAM_FILE, backup_file)
            logging.info(f"Created backup file before update: {backup_file}")

        show_progress_bar()

        # Download the new version from the server
        download_file(REMOTE_PROGRAM_URL, LOCAL_PROGRAM_FILE)

        # Validate the checksum of the downloaded file
        expected_checksum = fetch_file(REMOTE_CHECKSUM_URL)
        if not expected_checksum:
            raise Exception("Failed to fetch the expected checksum.")
        if not validate_checksum(LOCAL_PROGRAM_FILE, expected_checksum):
            raise Exception("Checksum validation failed.")

        # Update the version file with the new version information
        with open(LOCAL_VERSION_FILE, 'w') as f:
            f.write(fetch_file(REMOTE_VERSION_URL))
        logging.info("Updated to the latest version successfully.")
        print("Updated to the latest version successfully.")

    except Exception as e:
        logging.error(f"Error during update process: {e}")
        # Restore previous version from backup if it exists
        if backup_file and os.path.exists(backup_file):
            try:
                # Make sure to remove the failed update file before restoring the backup
                if os.path.exists(LOCAL_PROGRAM_FILE):
                    os.remove(LOCAL_PROGRAM_FILE)
                os.rename(backup_file, LOCAL_PROGRAM_FILE)
                logging.info(f"Restored previous version from backup: {backup_file}")
                print(f"An error occurred during the update: {e}. The previous version has been restored.")
            except Exception as restore_error:
                logging.error(f"Failed to restore previous version: {restore_error}")
                print(f"An error occurred during the update and failed to restore the previous version: {restore_error}")
        else:
            logging.error(f"Backup file: {backup_file} does not exist, unable to restore.")
            print(f"An error occurred during the update: {e}. The previous version could not be restored.")

# ------------- MAIN APPLICATION CODE -------------
def log_hello_world():
    """
    Log 'Hello world' and the current date and time to a txt file.
    """
    with open("hello_world.txt", "w") as file:
        file.write(f"Hello world - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main_program():
    """
    Main function representing the primary program logic.
    """
    log_hello_world()
    print("WERSJA SERWEROWA 11:41")

def main():
    """
    Main entry point for the update script. Handles command-line arguments
    and orchestrates the update process.
    """
    parser = argparse.ArgumentParser(description='Program updater.')
    parser.add_argument('--update', action='store_true', help='Update to the latest version')
    args = parser.parse_args()

    update_available, r_version, r_prefix = check_for_update()

    if args.update:
        if update_available:
            perform_update()
        else:
            print("You are already using the latest version.")
    else:
        if update_available:
            print("New version available. Use --update to download.")
        else:
            print("You are using the latest version.")
        main_program()

if __name__ == "__main__":
    main()
