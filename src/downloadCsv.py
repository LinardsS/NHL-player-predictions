from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import utils
from envVariables import getDataDirectory

def downloadPlayerSeasonStats(today, date, file_date):
    dataDirectory = getDataDirectory()
    directory = dataDirectory
    chromeOptions = Options()
    chromeOptions.add_experimental_option("prefs",{"download.default_directory": directory})

    if today is True:
        date_stamp = utils.getTodaysDate("%Y-%m-%d",backdate = True) # need to backdate due to NSS storing yesterday's file when accessing it in the morning
        file_datestamp = utils.getTodaysDate(backdate=True)
    else:
        date_stamp = date
        file_datestamp = file_date
    download_url = "https://www.naturalstattrick.com/playerteams.php?fromseason=20222023&thruseason=20222023&stype=2&sit=all&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=" + date_stamp + "&tgp=410&lines=single&draftteam=ALL"
    
    driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver\chromedriver.exe", chrome_options = chromeOptions)

    driver.get(download_url)

    driver.maximize_window()
    download_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.dt-button:nth-child(4)")))
    #click the download button
    download_button.click()
    time.sleep(3)
    driver.close()

    old_file = os.path.join(directory, "Player Season Totals - Natural Stat Trick.csv")
    new_file = os.path.join(directory, file_datestamp + " - Player Season Totals" + ".csv")
    os.rename(old_file, new_file)

def downloadTeamStats(today, date, file_date):
    dataDirectory = getDataDirectory()
    directory = dataDirectory
    chromeOptions = Options()
    chromeOptions.add_experimental_option("prefs",{"download.default_directory": directory})

    if today is True:
        date_stamp = utils.getTodaysDate("%Y-%m-%d",backdate = True) # need to backdate due to NSS storing yesterday's file when accessing it in the morning
        file_datestamp = utils.getTodaysDate(backdate=True)
    else:
        date_stamp = date
        file_datestamp = file_date
    download_url = "https://www.naturalstattrick.com/teamtable.php?fromseason=20222023&thruseason=20222023&stype=2&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td=";
    #uncomment below if need to download 2021-22 team data
    #download_url = "https://www.naturalstattrick.com/teamtable.php?fromseason=20212022&thruseason=20212022&stype=2&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td=";
    download_url = download_url + date_stamp

    driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver\chromedriver.exe", chrome_options = chromeOptions)

    driver.get(download_url)

    driver.maximize_window()
    download_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@value, 'CSV (All)')]")))
    #click the download button
    download_button.click()
    time.sleep(3)
    driver.close()

    old_file = os.path.join(directory, "games.csv")
    new_file = os.path.join(directory, file_datestamp + " - Team Season Totals" + ".csv")
    os.rename(old_file, new_file)

# downloadPlayerSeasonStats(today = False, date = "2022-10-07", file_date="07-10-22")
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
def downloadSeasonPlayerStats():
    start_date = date(2021, 10, 12)
    end_date = date(2022, 4, 29)
    for single_date in daterange(start_date, end_date):
        downloadPlayerSeasonStats(today = False, date = single_date.strftime("%Y-%m-%d"), file_date=single_date.strftime("%d-%m-%y"))
        print(single_date.strftime("%Y-%m-%d") + " processed")
#downloadSeasonPlayerStats()
#downloadPlayerSeasonStats(today = True, date = None, file_date = None)