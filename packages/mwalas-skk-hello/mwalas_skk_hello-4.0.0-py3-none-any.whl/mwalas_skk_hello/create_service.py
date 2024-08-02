import sys
from pathlib import Path
import shutil
import argparse

def create_service(user, group):
    """Creates and installs the systemd service file."""

    # Determine the current directory (where the script is located)
    script_dir = Path(__file__).parent

    # Determine Python version and application directory
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    app_home = Path.home() / f".local/lib/python{python_version}/site-packages/mwalas_skk_hello"
    venv_python = app_home / "venv/bin/python"
    log_file = app_home / "hello.log"

    # Path to the systemd service destination
    dest_file = Path("/etc/systemd/system/") / "mwalas-skk-hello.service"
    
    # Copy the service file to the systemd directory
    shutil.copy(script_dir / "mwalas-skk-hello.service", dest_file)

    # Create and write to the environment file
    env_file_path = Path("/etc/mwalas_skk_hello_env")
    with open(env_file_path, "w") as f:
        f.write(f"APP_HOME={app_home}\n")
        f.write(f"LOG_FILE={log_file}\n")

    # Replace placeholders in the service file with actual values
    with open(dest_file, "r") as f:
        content = f.read()

    content = content.replace("{{APP_HOME}}", str(app_home))
    content = content.replace("{{VENV_PYTHON}}", str(venv_python))
    content = content.replace("{{LOG_FILE}}", str(log_file))
    content = content.replace("{{USER}}", user)
    content = content.replace("{{GROUP}}", group)

    with open(dest_file, "w") as f:
        f.write(content)

    print("\nService file installed successfully at /etc/systemd/system/mwalas-skk-hello.service")
    print(f"Environment file created at {env_file_path}")

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
