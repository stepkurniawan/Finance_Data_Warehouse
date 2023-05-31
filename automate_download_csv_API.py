"""
Automate download csv, but using GET service of commerzbank API
getAccountTransactionsUsingGET
Resource URL: https://psd2.api.commerzbank.com/berlingroup/v1/accounts/{account-id}/transactions
Query Parameters
dateFrom
(required)	
Starting date of the transaction list -> date 1 of the previous month

dateTo	
End date of the transaction list -> last day of the previous month
"""

import os
import time
import requests
import json
import pandas as pd
from datetime import datetime, timedelta

#### VARIABLES ####
downloads_folder = os.path.join(os.path.expanduser("~"), "OneDrive", "Project", "Finance_Data_Lake", "Bank", "Commerzbank", "Auto_Download_CSV")

# Create the Downloads folder if it doesn't already exist
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

# Load the JSON file
with open('config.json') as f:
    config = json.load(f)

# Access the environment variable
oauth_client_id = config["COMMERZBANK_OAUTH_CLIENT_ID"]
oauth_secret = config["COMMERZBANK_OAUTH_SECRET"]
account_id = config["COMMERZBANK_ACCOUNT_ID"]

# Get the current date
today = datetime.today()

# Get the first day of the previous month
first_day_of_previous_month = datetime(today.year, today.month - 1, 1)

# Get the last day of the previous month
last_day_of_previous_month = datetime(today.year, today.month, 1) - timedelta(days=1)

# Format the dates to match the API's format
date_from = first_day_of_previous_month.strftime("%Y-%m-%d")
date_to = last_day_of_previous_month.strftime("%Y-%m-%d")

# Set the headers
headers = {
    #authorization base65 encoded
    "Authorization": f"Basic config["COMMERZBANK_OAUTH_BASE64"],
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

# Set the URL
# url = f"https://psd2.api.commerzbank.com/berlingroup/v1/accounts/{account_id}/transactions?dateFrom={date_from}&dateTo={date_to}"
url =   f"https://api-sandbox.commerzbank.com/api_operation HTTP/1.1"




# Get the response
response = requests.get(url, headers=headers)

# Convert the response to a JSON object
response_json = response.json()

# Get the transactions from the JSON object
transactions = response_json["transactions"]

# Convert the transactions to a DataFrame
df = pd.DataFrame(transactions)

# Convert the DataFrame to a CSV file
df.to_csv(os.path.join(downloads_folder, "commerzbank.csv"), index=False, sep=";")

