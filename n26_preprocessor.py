"""
This code is to preprocess the commerzbank csv file.
It must change the column names according to the google sheet.
The columns in google sheets: Timestamp	Date	Descriptions	Price	Category	Payment_Method		Location	Currency						

The commerzbank csv looks like: 
Date,"Payee","Account number","Transaction type","Payment reference","Amount (EUR)","Amount (Foreign Currency)","Type Foreign Currency","Exchange Rate"
2023-01-01,"From Main Account to My Entertainment","","Outgoing Transfer","Monthly Rule","-25.0","","",""

"""

import pandas as pd
import numpy as np


def preprocess_csv(input_file_path, output_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file_path, delimiter=",")

    # Rename columns
    df.rename(columns={
        "Date": "Timestamp",
        "Payee": "Payer",
        "Account number": "Account_Number",
        "Transaction type": "Transaction_Type",
        "Payment reference": "Descriptions",
        "Amount (EUR)": "Price",
        "Amount (Foreign Currency)": "Price_Foreign",
        "Type Foreign Currency": "Currency_Code",
        "Exchange Rate": "Exchange_Rate"
    }, inplace=True)

    # Add the "Category" column
    # TODO: Category can be more automated based on the "Description" column using regex or something
    df["Category"] = np.nan

    # Add the "Payment_Method" column
    df["Payment_Method"] = "N26"

    # Add the "Location" column 
    df["Location"] = "Germany"

    # Add the Currency column
    df["Currency"] = "EUR"

    # Set the datatypes of each columns
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%Y-%m-%d")
    df["Price"] = df["Price"].replace(",", ".").astype(float)
    df["Currency_Code"] = df["Currency_Code"].astype(str)
    df["Account_Number"] = df["Account_Number"].astype(str)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%Y-%m-%dT%H:%M:%S")
    df["Descriptions"] = df["Descriptions"].astype(str)
    df["Category"] = df["Category"].astype(str)
    df["Payment_Method"] = df["Payment_Method"].astype(str)
    df["Location"] = df["Location"].astype(str)
    df["Currency"] = df["Currency"].astype(str)

    # Save the DataFrame to a CSV file
    df.to_csv(output_file_path, index=False, sep=";")

    print("Preprocessing done and saved to ", output_file_path, "!")
    