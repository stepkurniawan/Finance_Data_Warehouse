"""
Use Selenium to download CSV of the current month from Commerzbank
This code will be run on the last day of each month automated using GitHub Actions.
It uses Selenium to go to the transaction page, filter the appropriate date, and download the CSV into the correct folder.
"""

import base64
import calendar
from datetime import date, timedelta
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

# Load the JSON file
with open('config.json') as f:
    config = json.load(f)

#### VARIABLES ####
base_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Project", "Finance_Data_Lake", "Bank")
com_downloads_folder = os.path.join(base_path, "Commerzbank", "Auto_Download_CSV")
n26_downloads_folder = os.path.join(base_path, "N26", "Auto_Download_CSV")

def commerzbank_selenium_download_csv(download_folder):  
    # Create the Downloads folder if it doesn't already exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Set the path to the Chrome driver
    chrome_driver_path = os.path.join(os.getcwd(), "chromedriver")

    # Set the options for the Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Create the Chrome driver
    driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)

    # Go to the Commerzbank login website
    driver.get("https://kunden.commerzbank.de/lp/login")

    # Wait for the page to load
    time.sleep(5)

    # Rejects all the cookies
    # Find and interact with the element using its ID
    element = driver.find_element(By.ID, 'uc-btn-deny-banner')
    element.click()

    # Access the environment variable
    username = config["COMMERZBANK_USERNAME"]
    com_pin = base64.b64decode(config["COMMERZBANK_PASSWORD"]).decode('utf-8') # the password is encoded in base64

    # Find the username and password fields and enter the username and password
    username_field = driver.find_element(By.ID, "teilnehmer")
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, "pin")
    password_field.send_keys(com_pin)

    # Find the page dropdown and select the "Kontoumsätze" option in German or "Account Transactions" in English
    # if the page dropdown was not found
    page_dropdown = Select(driver.find_element(By.ID, "startSite"))
    # select by value "/banking/account/transactionoverview"
    page_dropdown.select_by_value("/banking/account/transactionoverview")

    # Find the login button and click it
    login_button = driver.find_element(By.ID, "loginFormSubmit")
    login_button.click()

    # Wait for the page to load and user to enter the TAN
    time.sleep(20)

    #click download csv button
    parent_element = driver.find_element(By.ID, 'pageToggles')  # Replace with appropriate locator method
    csv_download_button = driver.find_element(By.CSS_SELECTOR, 'a[data-sel-id="csvButton"]')
    csv_download_button.click()

    # Wait for the CSV to be downloaded
    time.sleep(5)

    # logout by going to this link https://kunden.commerzbank.de/lp/logout
    driver.get("https://kunden.commerzbank.de/lp/logout")

    # Close the WebDriver manually
    driver.quit()


def n26_selenium_download_csv(download_folder):  
    # Create the Downloads folder if it doesn't already exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Set the path to the Chrome driver
    chrome_driver_path = os.path.join(os.getcwd(), "chromedriver")

    # Set the options for the Chrome driver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Create the Chrome driver
    driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)

    # Go to the n26 login website
    driver.get("https://app.n26.com/login")

    # Wait for the page to load
    time.sleep(5)

    # Access the environment variable
    username = config["COMMERZBANK_USERNAME"]
    password = base64.b64decode(config["N26_PASSWORD"]).decode('utf-8') # the password is encoded in base64

    # Find the username and password fields and enter the username and password
    username_field = driver.find_element(By.ID, "email")
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    # Find the login button and click it
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Wait for the page to load and user to enter the TAN
    time.sleep(25)

    #click download csv button
    csv_download_button = driver.find_element(By.CSS_SELECTOR, '[aria-labelledby="downloads-quick-action"]')
    csv_download_button.click()

    time.sleep(2)

    # check today date, if its 30 or 31, then use the curent month, else use the previous month
    today = date.today()
    if today.day == 30 or today.day == 31:
        start_date, end_date = calculate_date_current_month()
    else:
        start_date, end_date = calculate_date_previous_month()

    start_pick_date_input_field = driver.find_element(By.CSS_SELECTOR,'input.duet-date__input#start-date-picker')
    start_pick_date_input_field.clear()  
    start_pick_date_input_field.send_keys(start_date)

    end_pick_date_input_field = driver.find_element(By.CSS_SELECTOR,'input.duet-date__input#end-date-picker')
    end_pick_date_input_field.clear()
    end_pick_date_input_field.send_keys(end_date)

    # click the download button
    download_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    download_button.click()
    
    # Wait for the CSV to be downloaded
    time.sleep(5)
    
    # Close the WebDriver manually
    driver.quit()

    rename_file_to(start_date + "_" + end_date + ".csv")


# this function rename the file based to the input
def rename_file_to(new_name):
    # get the file path
    file_path = os.path.join(n26_downloads_folder, 'n26-csv-transactions.csv')
    # get the new file path
    new_file_path = os.path.join(n26_downloads_folder, new_name)
    # rename the file
    try:
        os.rename(file_path, new_file_path)
    except OSError:
        # if the file already exist, then overwrite it
        os.remove(new_file_path)
        os.rename(file_path, new_file_path)


# this function get the current date and calculate the date of the first and last date of the month
def calculate_date_current_month(): 
    # get the current date
    today = date.today()
    # get the first date of the month
    first_day_of_month = today.replace(day=1)
    # get the last date of the month
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    last_day_of_month = today.replace(day=last_day_of_month)
    # format date to be yyyy-mm-dd as a string
    first_day_of_month = first_day_of_month.strftime("%Y-%m-%d")
    last_day_of_month = last_day_of_month.strftime("%Y-%m-%d")

    return first_day_of_month, last_day_of_month

# calculate the previous month's first and last date
def calculate_date_previous_month():
    # get the current date
    today = date.today()
    # get previous month's date
    previous_month = today.replace(day=1) - timedelta(days=1)

    # get the first date of the previous month
    first_day_of_previous_month = previous_month.replace(day=1)
    # get the last date of the previous month
    last_day_of_previous_month = calendar.monthrange(previous_month.year, previous_month.month)[1]
    last_day_of_previous_month = previous_month.replace(day=last_day_of_previous_month)
    # format date to be yyyy-mm-dd as a string
    first_day_of_previous_month = first_day_of_previous_month.strftime("%Y-%m-%d")
    last_day_of_previous_month = last_day_of_previous_month.strftime("%Y-%m-%d")

    return first_day_of_previous_month, last_day_of_previous_month

