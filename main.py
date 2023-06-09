import upload_to_google_sheet as upload
import connect_to_google_sheet as connect
import commerzbank_preprocessor as com_preprocessor
import n26_preprocessor as n26_preprocessor
import automate_download_csv as automate_download_csv

def main():
    spreadsheet_id = "1WQFGfcp6PW8O5s0817yAkWIr-Am_mUvgjhaNAXjSCZU"
    credentials_file = "serviceAccount-cred.json"
    com_processed_file_path = "commerzbank.csv_preprocessed.csv"
    n26_processed_file_path = "n26_preprocessed.csv"
    com_sheet_name = "Commerz_Exp"
    redo_last_update = True

    #### Download the CSV file from the bank
    ### Commerzbank

    Banks = ["commerzbank", "n26"]

    # automate_download_csv.n26_selenium_download_csv()

    file_to_upload = upload.select_file_to_upload("n26")

    # if redo_last_update is true, then delete the last uploaded file from the upload tracker file
    if redo_last_update:
        upload.delete_last_uploaded_file_from_upload_tracker()

    if upload.check_if_file_already_uploaded(file_to_upload):
        print("File already uploaded. Exiting...")
        return
    else:
        print("File not uploaded yet. Continuing...")
        # com_preprocessor.preprocess_commerzbank_csv(file_to_upload, com_processed_file_path)
        n26_preprocessor.preprocess_n26_csv(file_to_upload, n26_processed_file_path)
        # com_sheet = connect.connect_to_google_sheet_and_get_sheet(spreadsheet_id, com_sheet_name, credentials_file)
        n26_sheet = connect.connect_to_google_sheet_and_get_sheet(spreadsheet_id, "N26_Exp", credentials_file)
        # upload.upload_to_google_sheet(com_processed_file_path, com_sheet)
        upload.upload_to_google_sheet(n26_processed_file_path, n26_sheet)
        upload.update_upload_tracker(n26_processed_file_path)


if __name__ == "__main__":
    main()