from subprocess import run, TimeoutExpired, CalledProcessError
import time

import warnings 
warnings.filterwarnings('ignore') 
import pandas as pd
from email_script import send_email

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

fls = ['download_info.py']
while True:
    for file in fls:
        try:
            try:
                temp_df_sme = pd.read_csv("sme_output.csv")
                temp_df_cm = pd.read_csv("cm_output.csv")
            except:
                temp_df_sme = pd.DataFrame()
                temp_df_cm = pd.DataFrame()
            run(["python", file], check=True, timeout=60)  # seconds timeout
            print("scraped :)", file)
            final_df_sme = pd.read_csv("sme_output.csv")
            final_df_cm = pd.read_csv("cm_output.csv")
            print("changes in sme")
            print(final_df_sme.merge(temp_df_sme, how='outer', indicator=True).query('_merge == "left_only"').drop('_merge', 1))
            print("changes in cm")
            print(final_df_cm.merge(temp_df_cm, how='outer', indicator=True).query('_merge == "left_only"').drop('_merge', 1))
            col_list = final_df_cm.columns
            sme_only_new = final_df_sme.merge(temp_df_sme, how='outer', indicator=True).query('_merge == "left_only"').drop('_merge', 1)
            cm_only_new = final_df_cm.merge(temp_df_cm, how='outer', indicator=True).query('_merge == "left_only"').drop('_merge', 1)
            # print(sme_only_new)
            # print(cm_only_new)
            send_email(sme_only_new)
            send_email(cm_only_new)
        except TimeoutExpired:
            message = "Timeout :( !!!"
            print(message, file)
            # f.write("{message} {file}\n".format(file=file, message=message))
        except CalledProcessError:
            message = "SOMETHING HAPPENED :( !!!, CHECK"
            print(message, file)
            # f.write("{message} {file}\n".format(file=file, message=message))
    l = 60
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, item in enumerate(list(range(0,l))):
        # Do stuff...
        time.sleep(1)
        # Update Progress Bar
        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)