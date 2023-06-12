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
com_dir_download_csv = os.path.join(base_path, "Commerzbank", "Auto_Download_CSV")
n26_dir_download_csv = os.path.join(base_path, "N26", "Auto_Download_CSV")

commerzbank = Bank(name="commerzbank", 
                    preprocessor=com_preprocessor ,
                    selenium_download_csv=lambda: automate_download_csv.commerzbank_selenium_download_csv(com_dir_download_csv),
                    google_sheet_name="commerzbank_Exp", 
                    processed_file_path="commerzbank_preprocessed.csv", 
                    dir_download_csv=com_dir_download_csv
)

n26 = Bank(name="n26",
            preprocessor=n26_preprocessor,
            selenium_download_csv=lambda: automate_download_csv.n26_selenium_download_csv(n26_dir_download_csv),
            google_sheet_name="n26_Exp",
            processed_file_path="n26_preprocessed.csv",
            dir_download_csv=n26_dir_download_csv
            )

def main():
    Banks = [commerzbank, n26]

    for bank in Banks:
        print("Starting upload pipeline for ", bank.name)

        # download csv from the bank website
        bank.selenium_download_csv()

        # find the most recent file
        file_to_upload = upload.select_file_to_upload(bank.dir_download_csv)

        if skip_check_and_directly_upload:
            print("Skipping the tracker check and directly upload.")
            upload_pipeline(bank, file_to_upload)
        else:
            if upload.check_if_file_already_uploaded(file_to_upload):
                break
            else:
                upload_pipeline(bank, file_to_upload)


def upload_pipeline(bank, file_to_upload):
    print("#### starting upload pipeline")
    bank.preprocessor.preprocess_csv(file_to_upload, bank.processed_file_path)
    print("preprocessing bank ", bank.name, " done")

    sheet = connect.connect_to_google_sheet_and_get_sheet(spreadsheet_id, bank.google_sheet_name, credentials_file)
    print("connected to google sheet ", bank.google_sheet_name)

    upload.upload_to_google_sheet(bank.processed_file_path, sheet)
    print("upload to google sheet ", bank.google_sheet_name, " done")

    upload.update_upload_tracker(file_to_upload)
    print("upload tracker updated")



if __name__ == "__main__":
    main()