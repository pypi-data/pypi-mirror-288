"""Script to create and install the systemd service for mwalas-skk-hello."""

import sys
from pathlib import Path
import shutil
import argparse

def create_service(user, group):
    """Creates and installs the systemd service file."""

    # Determine the current directory (where the script is located)
    script_dir = Path(__file__).parent

    # Path to the service file in the same directory as the script
    service_file_path = script_dir / "mwalas-skk-hello.service"

    if not service_file_path.is_file():
        raise FileNotFoundError("Service file not found in the current directory")

    # Path to the systemd service destination
    dest_file = Path("/etc/systemd/system/") / "mwalas-skk-hello.service"
    shutil.copy(service_file_path, dest_file)

    # Replace placeholders in the service file with actual values
    with open(dest_file, "r") as f:
        content = f.read()
    content = content.replace("{{APP_HOME}}", str(script_dir))
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
