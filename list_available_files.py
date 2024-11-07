import requests
import pandas as pd
import toml

def list_available_files():
    
    # get variables for API call
    with open('config.toml', 'r') as f:
        config = toml.load(f)
        
    base_endpoint = config['API-details']['base_endpoint']
    package_list_method = config['API-details']['package_list_method']
    package_show_method = config['API-details']['package_show_method']
    action_method = config['API-details']['action_method']
    
    dataset_id = config['dataset']['dataset_id']

    # call metadata to see which files are available
    metadata_response = requests.get(f"{base_endpoint}"\
                                    f"{package_show_method}"\
                                    f"{dataset_id}").json()

    # find resource names and IDs
    resources_table = pd.json_normalize(metadata_response['result']['resources'])
    
    # create CSV with list of available files
    resources_table.to_csv('output/available_files.csv', index = False)