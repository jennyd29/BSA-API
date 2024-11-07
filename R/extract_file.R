library(jsonlite)
library(dplyr)
library(crul)

# define parameters for API call
source("R/config.R")

# send API call
datasets_response <- jsonlite::fromJSON(paste0(
  base_endpoint, package_list_method
))

# check available datasets
datasets_response$result

# create SQL query
single_month_query <- paste0(
  "
  SELECT 
      * 
  FROM `", 
  resource_name, "`" 
)

# API call for query
single_month_api_call <- paste0(
  base_endpoint,
  action_method,
  "resource_id=",
  resource_name, 
  "&",
  "sql=",
  URLencode(single_month_query)
)

# return response as json list
single_month_response <- jsonlite::fromJSON(single_month_api_call)

# convert to a dataframe
df <- single_month_response$result$result$records

# write to csv file
write.csv(df, "R/single_table_output.csv", row.names = FALSE)
