import os
import json
import requests

# Function to create mod directory and download mods
def download_mods(manifest_file: str, api_key: str):
    # Load manifest file
    with open(manifest_file, 'r') as file:
        manifest = json.load(file)
    
    # Create mods directory
    mods_dir = 'mods'
    os.makedirs(mods_dir, exist_ok=True)
    
    # Download each mod file
    for file_info in manifest['files']:
        project_id = file_info['projectID']
        file_id = file_info['fileID']
        download_url_api = f"https://api.curseforge.com/v1/mods/{project_id}/files/{file_id}/download-url"

        headers = {
            'Accept': 'application/json',
            'x-api-key': api_key
        }

        try:
            # Get the download URL
            response = requests.get(download_url_api, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

            # Extract the actual download URL from the response
            download_url = response.json().get('data')
            if not download_url:
                print(f"No download URL found for projectID {project_id}, fileID {file_id}.")
                continue

            # Download the mod file
            mod_response = requests.get(download_url)
            mod_response.raise_for_status()

            mod_file_path = os.path.join(mods_dir, download_url.split("/")[-1])
            with open(mod_file_path, 'wb') as mod_file:
                mod_file.write(mod_response.content)
            print(f"Downloaded: {mod_file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download projectID {project_id}, fileID {file_id}: {e}")

# Specify that the manifest.json file is in the same directory
manifest_file_path = 'manifest.json'  # File is in the same directory
api_key = '$2a$10$ViK4qJmgrAUnA034XsP6mezlZJOMDljncIvCLwXjNtF/tfBj02Qta'

# Call the function
download_mods(manifest_file_path, api_key)  