"""Script to create and install the systemd service for mwalas-skk-hello."""

import sys
from pathlib import Path
import shutil
import argparse
import pkg_resources

def create_service(user, group):
    """Creates and installs the systemd service file."""

    # Determine Python version and package installation directory
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    app_home = Path.home() / f".local/lib/python{python_version}/site-packages/mwalas_skk_hello"

    # Create an empty .env file in the package directory
    env_file = app_home / ".env"
    env_file.touch()

    # Find the path to the service file within the installed package
    try:
        service_file_path = pkg_resources.resource_filename("mwalas_skk_hello.scripts", "mwalas-skk-hello.service")
    except FileNotFoundError:
        raise FileNotFoundError("Service file not found in the package")

    dest_file = Path("/etc/systemd/system/") / "mwalas-skk-hello.service"
    shutil.copy(service_file_path, dest_file)

    # Replace placeholders in the service file with actual values
    with open(dest_file, "r") as f:
        content = f.read()
    content = content.replace("{{APP_HOME}}", str(app_home))
    content = content.replace("{{USER}}", user)
    content = content.replace("{{GROUP}}", group)
    with open(dest_file, "w") as f:
        f.write(content)

    print("\nService file installed successfully at /etc/systemd/system/mwalas-skk-hello.service")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create and install the systemd service for mwalas-skk-hello.")
    parser.add_argument("--user", required=True, help="The user to run the service as.")
    parser.add_argument("--group", required=True, help="The group to run the service as.")
    args = parser.parse_args()

    create_service(args.user, args.group)

    # Inform the user about the next steps
    print("\nInstallation complete. To start the service, run the following commands:")
    print("sudo systemctl daemon-reload")
    print("sudo systemctl enable mwalas-skk-hello.service")
    print("sudo systemctl start mwalas-skk-hello.service")
