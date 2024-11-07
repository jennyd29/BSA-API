import urllib.parse
import requests
import pandas as pd
import toml

def extract_file():
    
    # get variables for API call
    with open('python/config.toml', 'r') as f:
        config = toml.load(f)
        
    base_endpoint = config['API-details']['base_endpoint']
    package_list_method = config['API-details']['package_list_method']
    package_show_method = config['API-details']['package_show_method']
    action_method = config['API-details']['action_method']
    
    resource_name = config['single-file']['resource_name']
    
    # sql query for CONTRACT_ANNUAL_201604
    single_month_query = "SELECT * " \
                        f"FROM `{resource_name}`"

    # API call for query
    single_month_api_call = f"{base_endpoint}" \
                            f"{action_method}" \
                            "resource_id=" \
                            f"{resource_name}" \
                            "&" \
                            "sql=" \
                            f"{urllib.parse.quote(single_month_query)}" # Encode spaces in the url
                            
    # extract response as json list
    response = requests.get(single_month_api_call).json()
    response

    # convert to dataframe
    df = pd.json_normalize(response['result']['result']['records'])
    
    # write csv
    df.to_csv('python/output/single_table.csv', index = False)