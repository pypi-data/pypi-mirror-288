import subprocess
import os
import threading

from fastapi import HTTPException

from cass_api.ctags.util import generate_ctags

# Create a global lock for thread safety
lock = threading.Lock()

# Define paths
target_sdk_path = './fern_config/sdks/python/src/'
fern_config_path = './fern_config'

def run_command(command, cwd=None):
    """
    Run a shell command and handle errors.
    """
    try:
        if cwd:
            cwd = os.path.abspath(cwd)

        full_command = command
        if os.path.exists(os.path.expanduser("~/.nvm")):
            full_command = f"bash -c 'export NVM_DIR=\"$HOME/.nvm\" && source $NVM_DIR/nvm.sh && nvm use lts/iron && {command}'"
        result = subprocess.run(full_command, check=True, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"Output: {e.output}")
        print(f"Error Output: {e.stderr}")

def generate_sdk(openapi_content, ctags_file_name):
    """
    Write the openapi.yaml content to the specified destination and generate the SDK.
    """
    openapi_destination = os.path.join(fern_config_path, 'fern/openapi/openapi.yaml')

    with lock:
        os.makedirs(os.path.dirname(openapi_destination), exist_ok=True)
        with open(openapi_destination, 'w') as file:
            file.write(openapi_content)

        try:
            # Run the fern generate commands
            print(run_command(f'fern generate --group python-sdk', cwd=fern_config_path))

            # Generate ctags
            generate_ctags(target_sdk_path, f"./tenant_ctags/{ctags_file_name}")

        except subprocess.CalledProcessError as e:
            print(f"Error generating SDK: {e}")
            HTTPException(status_code=500, detail="Error generating SDK")