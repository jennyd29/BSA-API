import requests
import csv
import toml

def list_available_datasets(): 
    
    # get variables for API call
    with open('python/config.toml', 'r') as f:
        config = toml.load(f)
        
    base_endpoint = config['API-details']['base_endpoint']
    package_list_method = config['API-details']['package_list_method']
    package_show_method = config['API-details']['package_show_method']
    action_method = config['API-details']['action_method']

    # send API call
    datasets_response = requests.get(base_endpoint + package_list_method)
    datasets_response = datasets_response.json()

    # create CSV with list of available datasets
    with open ('python/output/available_datasets.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow(datasets_response['result'])