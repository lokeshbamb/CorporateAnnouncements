import pandas as pd
import requests

def data_download():
  sme_url = "https://www.nseindia.com/api/corporate-announcements?index=sme&csv=true"
  cm_url = "https://www.nseindia.com/api/corporate-announcements?index=equities&csv=true"
  payload = {}
  headers = {
    'authority': 'www.nseindia.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://www.nseindia.com/companies-listing/corporate-filings-announcements',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
  }

  from selenium.common.exceptions import StaleElementReferenceException
  import time, glob, os
  import undetected_chromedriver as uc
  from seleniumwire import webdriver
  from selenium.webdriver.chrome.service import Service

  service = Service(executable_path="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  # options = ['--headless']
  # options.add_argument('--no-sandbox')
  # options.add_argument('--disable-dev-shm-usage')
  # options.add_argument('ignore-certificate-errors')
  print("hi")
  driver = webdriver.Chrome()
  driver.get("https://www.nseindia.com/companies-listing/corporate-filings-announcements")

  for request in driver.requests:
      # print(request.headers)
      # print(request.headers.keys())
      if "cookie" in list(request.headers.keys()):
        # print("cookies added")
        headers['cookie'] = request.headers['cookie']

  update_no = [0,0]
  for url in [sme_url, cm_url]:
    response = requests.request("GET", url, headers=headers, data=payload)

    s = str(response.content, "utf-8")
    l = s.split("\n")
    data = []
    for i in l:
        data.append(i.split('","'))
    # for i in data:
    #   print(len(i))
    # print(data[3])
    df = pd.DataFrame(columns=data[0], data=data[1:])
    df.replace('"', '', regex=True, inplace=True)
    # print(df)
    try:
      if url == sme_url:
        out_df = pd.read_csv('sme_output.csv')
      else:
         out_df = pd.read_csv('cm_output.csv')
    except:
        out_df = pd.DataFrame()
    final_df = df.append(out_df)
    final_df.drop_duplicates(inplace=True, ignore_index=True)
    # print(final_df)
    update_col = final_df.shape[0] - out_df.shape[0]
    # print(final_df.head(update_col))
    if len(df.columns) == 10:
       continue
    if url == sme_url:
      # df = pd.read_csv('sme_output.csv')
      # df = df.tail(100)
      update_no[0] = update_col
      final_df.to_csv('sme_output.csv', index=False)
    else:
      update_no[1] = update_col
      final_df.to_csv('cm_output.csv', index=False)
    # df = pd.read_csv(str(response.content, "utf-8"), sep=",")
    # print(df)
  return update_no

update_no = data_download()
print(update_no)