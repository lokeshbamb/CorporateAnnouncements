from selenium.common.exceptions import StaleElementReferenceException
import time, glob, os
import undetected_chromedriver as uc
from os.path import join

def download_corp_action(driver, action_type):
    purpose_dict = {"Bonus" : "P5", "Dividend" : "P9", "StockSplit" : "P26"}

    if not driver:
        raise ValueError("ChromeDriver needs to be provided to download data.")

    if not action_type:
        raise ValueError("You need to mention the corp action type, allowable fields ['dividend', 'split', 'bonus']")

    if not isinstance(action_type, str):
        raise ValueError("action_type arguement needs to be a str.")

    action_type =  action_type.lower()

    if action_type not in ['dividend', 'split', 'bonus']:
        raise ValueError("Incorrect Corporate Action Input, allowable fields ['dividend', 'split', 'bonus']")
    
    print(dir(driver))
    # exit(0)
    purpose = driver.find_element("xpath", '//*[@id="ddlPurpose"]')

    purpose.click()

    if action_type == 'dividend':
        corp_act = purpose_dict['Dividend']
    elif action_type == 'split':
        corp_act = purpose_dict['StockSplit']
    else:
        corp_act = purpose_dict['Bonus']

    selected_purpose = driver.find_element("xpath", f'//*[@id="ddlPurpose"]/option[@value=\"{corp_act}\"]')

    try:
        selected_purpose.click()
    except StaleElementReferenceException:
        selected_purpose = driver.find_element("xpath", f'//*[@id="ddlPurpose"]/option[@value=\"{corp_act}\"]')
        selected_purpose.click()

    submit = driver.find_element("xpath", '//*[@id="btnSubmit"]')
    submit.click()

    time.sleep(5)

    download_csv = driver.find_element("xpath", '//*[@id="lnkDownload"]')

    try:
        download_csv.click()
    except StaleElementReferenceException:
        download_csv = driver.find_element("xpath", '//*[@id="lnkDownload"]')
        download_csv.click()


def get_latest_file(path):
    list_of_files = glob.glob(f'{path}/Corporate_Actions*.csv')
    try:
        latest_file = max(list_of_files, key = os.path.getctime)
    except ValueError:
        time.sleep(10)
        try:
            latest_file = max(list_of_files, key = os.path.getctime)
        except ValueError:
            raise ValueError("Sorry, we are not able to download data from BSE website.")

    return latest_file

def rename_latest_file(filepath, newfilepath):
    try:
        os.rename(filepath,newfilepath)
    except FileExistsError:
        os.remove(newfilepath)
        os.rename(filepath, newfilepath)
    except FileNotFoundError:
        raise ValueError("Sorry, we are not able to download data from BSE website.")

def corporate_actions():
    bse_corp_path = 'https://www.bseindia.com/corporates/corporate_act.aspx'

    default_downloads_path = join('C:', os.sep, 'Users', os.getlogin(), 'Downloads')

    options = uc.ChromeOptions() 
    options.add_argument("--headless")
    driver = uc.Chrome(options=options)
    driver.get(bse_corp_path)
    download_corp_action(driver, 'dividend')
    time.sleep(15)
    latest_file = get_latest_file(default_downloads_path)
    rename_latest_file(latest_file, f'{default_downloads_path}/dividend.csv')
    
    download_corp_action(driver, 'split')
    time.sleep(5)
    latest_file = get_latest_file(default_downloads_path)
    rename_latest_file(latest_file, f'{default_downloads_path}/split.csv')
    
    download_corp_action(driver, 'bonus')
    time.sleep(5)
    latest_file = get_latest_file(default_downloads_path)
    rename_latest_file(latest_file, f'{default_downloads_path}/bonus.csv')
    
    driver.close()

if __name__ == "__main__":

    corporate_actions()
