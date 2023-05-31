import pandas as pd
import gspread
import connect_to_google_sheet as connection
import os
from gspread_dataframe import set_with_dataframe, get_as_dataframe
import time

def select_file_to_upload():
    print("Selecting file to upload...")

    # go to the downloads folder
    downloads_folder = os.path.join(os.path.expanduser("~"), "OneDrive", "Project", "Finance_Data_Lake", "Bank", "Commerzbank", "Auto_Download_CSV")

    # get all the files in the folder
    files = os.listdir(downloads_folder)

    if not files:
        raise FileNotFoundError("No files found in the downloads folder.")

    # Sort the files by date
    try:
        files.sort(key=os.path.getmtime)
    except OSError as e:
        print(f"Error occurred while sorting files: {e}")
        


    # get the most recent file
    file = files[-1]

    # get the file path
    file_path = os.path.join(downloads_folder, file)

    print("File selected!")
    return file_path

    

def upload_to_google_sheet(file_path, sheet):
    print("Uploading to Google Sheet...")
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, delimiter=";")

    # Convert all columns to string to avoid InvalidJSONError: Out of range float values are not JSON compliant
    df = df.astype(str)

    # Get the existing headers (column names) from the sheet
    existing_headers = sheet.row_values(1)

    # Add new columns to the sheet if they don't already exist
    new_columns = [col for col in df.columns if col not in existing_headers]
    if new_columns:
        num_existing_columns = len(existing_headers)
        new_headers_range = sheet.range(1, num_existing_columns + 1, 1, num_existing_columns + len(new_columns))
        for header_cell, new_column in zip(new_headers_range, new_columns):
            header_cell.value = new_column
        sheet.update_cells(new_headers_range)

    # Reorder the columns in the DataFrame to match the sheet's columns
    df = df.reindex(columns=existing_headers)

    # Convert float values to strings with limited precision
    float_columns = df.select_dtypes(include=float).columns
    df[float_columns] = df[float_columns].applymap(lambda x: f"{x:.2f}")


    # Append the DataFrame to the sheet
    data = df.values.tolist()
    sheet.append_rows(data)

    # Add a delay of 1 second between each API call
    time.sleep(1)
    print("Upload complete!")