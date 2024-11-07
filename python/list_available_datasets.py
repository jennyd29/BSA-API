import requests
import csv

def list_available_datasets(): 
    
    # define variables for API call
    base_endpoint = 'https://opendata.nhsbsa.net/api/3/action/'
    package_list_method = 'package_list'
    package_show_method = 'package_show?id='
    action_method = 'datastore_search_sql?' 

    # send API call
    datasets_response = requests.get(base_endpoint + package_list_method)
    datasets_response = datasets_response.json()

    # create CSV with list of available datasets
    with open ('output/available_datasets.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow(datasets_response['result'])