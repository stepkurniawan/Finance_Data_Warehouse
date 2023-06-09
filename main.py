import os
import upload_to_google_sheet as upload
import connect_to_google_sheet as connect
import commerzbank_preprocessor as com_preprocessor
import n26_preprocessor as n26_preprocessor
import automate_download_csv as automate_download_csv
from bank_class import Bank


spreadsheet_id = "1WQFGfcp6PW8O5s0817yAkWIr-Am_mUvgjhaNAXjSCZU"
credentials_file = "serviceAccount-cred.json"
skip_check_and_directly_upload = False
base_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Project", "Finance_Data_Lake", "Bank")

def main():
    commerzbank = Bank(name="commerzbank", 
                        preprocessor=com_preprocessor ,
                        selenium_download_csv=lambda: automate_download_csv.commerzbank_selenium_download_csv(dir_download_csv),
                        google_sheet_name="commerzbank_Exp", 
                        processed_file_path="commerzbank_preprocessed.csv", 
                        dir_download_csv=os.path.join(base_path, "Commerzbank", "Auto_Download_CSV"))
    
    n26 = Bank(name="n26",
                preprocessor=n26_preprocessor,
                selenium_download_csv=lambda: automate_download_csv.n26_selenium_download_csv(dir_download_csv),
                google_sheet_name="n26_Exp",
                processed_file_path="n26_preprocessed.csv",
                dir_download_csv=os.path.join(base_path, "N26", "Auto_Download_CSV"))

    Banks = [commerzbank, n26]

    for bank in Banks:
        print("Starting upload pipeline for ", bank.name)

        # download csv from the bank website
        bank.selenium_download_csv

        # find the most recent file
        file_to_upload = upload.select_file_to_upload(n26.dir_download_csv)

        if skip_check_and_directly_upload:
            print("Skipping the tracker check and directly upload.")
            upload_pipeline(n26)
        else:
            if upload.check_if_file_already_uploaded(file_to_upload):
                return
            else:
                upload_pipeline(n26)

if __name__ == "__main__":
    main()

def upload_pipeline(bank):
    print("#### starting upload pipeline")
    bank.preprocessor.preprocess_csv(bank.dir_download_csv, bank.processed_file_path)
    print("preprocessing bank ", bank.name, " done")

    sheet = connect.connect_to_google_sheet_and_get_sheet(spreadsheet_id, bank.google_sheet_name, credentials_file)
    print("connected to google sheet ", bank.google_sheet_name)

    upload.upload_to_google_sheet(bank.processed_file_path, sheet)
    print("upload to google sheet ", bank.google_sheet_name, " done")

    upload.update_upload_tracker(bank.processed_file_path)
    print("upload tracker updated")
