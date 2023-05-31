import upload_to_google_sheet as upload
import connect_to_google_sheet as connect
import commerzbank_preprocessor as com_preprocessor


def main():
    spreadsheet_id = "1WQFGfcp6PW8O5s0817yAkWIr-Am_mUvgjhaNAXjSCZU"
    credentials_file = "serviceAccount-cred.json"
    com_processed_file_path = "commerzbank.csv_preprocessed.csv"
    com_sheet_name = "Commerz_Exp"

    file_to_upload = upload.select_file_to_upload()
    

    if upload.check_if_file_already_uploaded(file_to_upload):
        print("File already uploaded. Exiting...")
        return
    else:
        print("File not uploaded yet. Continuing...")
        com_preprocessor.preprocess_commerzbank_csv(file_to_upload, com_processed_file_path)
        com_sheet = connect.connect_to_google_sheet_and_get_sheet(spreadsheet_id, com_sheet_name, credentials_file)
        upload.upload_to_google_sheet(com_processed_file_path, com_sheet)
        upload.update_upload_tracker(file_to_upload)


if __name__ == "__main__":
    main()