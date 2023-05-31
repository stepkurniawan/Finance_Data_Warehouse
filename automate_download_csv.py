"""
Use Selenium to download CSV of the current month from Commerzbank
This code will be run on the last day of each month automated using GitHub Actions.
It uses Selenium to go to the transaction page, filter the appropriate date, and download the CSV into the correct folder.
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

#### VARIABLES ####
downloads_folder = os.path.join(os.path.expanduser("~"), "OneDrive", "Project", "Finance_Data_Lake", "Bank", "Commerzbank", "Auto_Download_CSV")

# Create the Downloads folder if it doesn't already exist
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

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
    "download.default_directory": downloads_folder,
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

# Load the JSON file
with open('config.json') as f:
    config = json.load(f)

# Access the environment variable
username = config["COMMERZBANK_USERNAME"]
com_pin = config["COMMERZBANK_PASSWORD"]

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