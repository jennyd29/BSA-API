import urllib.parse
import requests
import pandas as pd
import toml
import csv

def extract_time_series():
    
    # get variables for API call
    with open('python/config.toml', 'r') as f:
        config = toml.load(f)
        
    base_endpoint = config['API-details']['base_endpoint']
    package_list_method = config['API-details']['package_list_method']
    package_show_method = config['API-details']['package_show_method']
    action_method = config['API-details']['action_method']
    
    dataset_id = config['dataset']['dataset_id']
    year = config['time-series']['year']
    
    # return list of tables available
    metadata_response = requests.get(f"{base_endpoint}" \
                                    f"{package_show_method}" \
                                    f"{dataset_id}").json()
    
    # filter for resource names in the specified year
    resources_table = pd.json_normalize(metadata_response['result']['resources'])
    resource_name_list = resources_table[resources_table['name'].str.contains('2020')]['name']
    
    # create for loop to combine API calls into data frame
    for_loop_df = pd.DataFrame()
    
    # loop through resource name, make API call, then bind into data frame
    for file in resource_name_list:
        
        # temporary SQL query
        tmp_query = "SELECT * " \
                    f"FROM `{file}` "
        
        # temporary API call
        tmp_api_call = f"{base_endpoint}" \
                        f"{action_method}" \
                        "resource_id=" \
                        f"{file}" \
                        "&" \
                        "sql=" \
                        f"{urllib.parse.quote(tmp_query)}" # Encode spaces in the url
        
        # temporary json response
        tmp_response = requests.get(tmp_api_call).json()
        
        # extract record into temporary data frame
        tmp_df = pd.json_normalize(tmp_response['result']['result']['records'])
        
        # bind temporary df to main df
        for_loop_df = pd.concat([for_loop_df, tmp_df])
        
    # write csv
    for_loop_df.to_csv('python/output/time_series.csv', index = False)
    
extract_time_series()