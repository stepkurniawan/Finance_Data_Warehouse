"""
This code is to preprocess the commerzbank csv file.
It must change the column names according to the google sheet.
The columns in google sheets: Timestamp	Date	Descriptions	Price	Category	Payment_Method		Location	Currency						

The commerzbank csv looks like: 
Buchungstag	Wertstellung	Umsatzart	Buchungstext	Betrag	Währung	Auftraggeberkonto	Bankleitzahl Auftraggeberkonto	IBAN Auftraggeberkonto
28.02.2022	28.02.2022	Lastschrift	PENNY SAGT DANKE. 31300291//Luenebu 2022-02-26T20:35:28 KFN 0 VJ 2212 Kartenzahlung	-9,01	EUR	611093600	48040035	DE06480400350611093600

"""

import pandas as pd
import numpy as np

def preprocess_csv(input_file_path, output_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file_path, delimiter=";")

    # Rename columns
    df.rename(columns={
        "Buchungstag": "Timestamp",
        "Wertstellung": "Value_Date",
        "Umsatzart": "Payment_Method_Details",
        "Buchungstext": "Description",
        "Betrag": "Price",
        "Währung": "Currency",
        "Auftraggeberkonto": "Sender_Account_Number",
        "Bankleitzahl Auftraggeberkonto": "Sender_Bank_Code",
        "IBAN Auftraggeberkonto": "Sender_IBAN"
    }, inplace=True)


    # Add the "Category" column
    # TODO: Category can be more automated based on the "Description" column using regex or something
    df["Category"] = np.nan

    # Add the "Payment_Method" column
    df["Payment_Method"] = "Commerzbank"

    # Add the "Location" column
    df["Location"] = "Germany"

    # Set the datatypes of each columns
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%d.%m.%Y")
    df["Value_Date"] = pd.to_datetime(df["Value_Date"], format="%d.%m.%Y")
    df["Price"] = df["Price"].str.replace(",", ".").astype(float)
    df["Currency"] = df["Currency"].astype(str)
    df["Sender_Account_Number"] = df["Sender_Account_Number"].astype(str)
    df["Sender_Bank_Code"] = df["Sender_Bank_Code"].astype(str)
    df["Sender_IBAN"] = df["Sender_IBAN"].astype(str)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%Y-%m-%dT%H:%M:%S")
    df["Payment_Method_Details"] = df["Payment_Method_Details"].astype(str)
    df["Description"] = df["Description"].astype(str)
    df["Category"] = df["Category"].astype(str)
    df["Payment_Method"] = df["Payment_Method"].astype(str)
    df["Location"] = df["Location"].astype(str)

    


    #### Filter the data frame, leaving the unnecessary columns behind
    df_filtered = df[["Timestamp", "Description", "Price", "Category", "Payment_Method", "Location", "Currency"]]

    # remove the rows when the "Price" column is positive (it means income)
    df_filtered = df_filtered[df_filtered["Price"] < 0]

    # Write the DataFrame to a CSV file
    df_filtered.to_csv(output_file_path, index=False, sep=";")

if __name__ == "__main__":
    input_file_path = "commerzbank.csv"
    output_file_path = input_file_path+"_preprocessed.csv"
    preprocess_csv(input_file_path, output_file_path)

