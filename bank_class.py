class Bank:
    def __init__(self, name, preprocessor, selenium_download_csv, google_sheet_name, processed_file_path, dir_download_csv):
        self.name = name
        self.preprocessor = preprocessor
        self.selenium_download_csv = selenium_download_csv
        self.google_sheet_name = google_sheet_name
        self.processed_file_path = processed_file_path
        self.dir_download_csv = dir_download_csv 
