import datetime, time
import requests
import os
import glob

import configparser
import logging
import traceback

from win10toast import ToastNotifier
import six
import appdirs
import packaging.requirements
import validators
import urllib.request

from helper import itembases, filteradds, get_random_filtername

import ctypes


# load config from file
config = configparser.ConfigParser(interpolation=None)
config.read("config.ini")

if config.getboolean("settings", "minimize_on_start"):
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )

# setup logger
logging_handler = [logging.StreamHandler()]
if config.getboolean("settings", "log_to_file"):
    logging_handler.append(logging.FileHandler("log.txt"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=logging_handler
)
logging.info("Starting.")


# create first request to get all tab names of character
url = "https://www.pathofexile.com/character-window/get-stash-items"
cookies = {
    "POESESSID": config.get("poeinfo", "poesessid")
}
payload = {
    "tabs":1, 
    "league": config.get("poeinfo", "league"), 
    "accountName": config.get("poeinfo", "account_name")
}

logging.info("Requesting tab info.")
resp = requests.get(url, params=payload, cookies=cookies)
logging.info(f"GET request returned status_code {resp.status_code}.")
resp = resp.json()

# look for named tab and modify future payloads accordingly
for tab in resp["tabs"]:
    if tab["n"] == config.get("poeinfo", "tabname"):
        payload["tabIndex"]=tab["i"]
        payload["tabs"]=0
        break
     

# just a string to help split the filter
split_helper = "#imjustalinetohelptosplitthefileproperlyjustignoreme"

if config.getboolean("settings", "toast_alert"):
    logging.info("Creating ToastNotifier.")
    toaster = ToastNotifier()


# check what filter to change
logging.info("Checking filter path.")
filterpath = config.get("filter", "filterpath")

if validators.url(filterpath):
    poedir = os.environ["userprofile"] + "\Documents\My Games\Path of Exile\\"
    filtername = "chaosrecipehelper.filter"
    targetpath = os.path.join(poedir, filtername)

    logging.info(f"Filterpath in config is url, downloading filter into {targetpath}.")
    urllib.request.urlretrieve(config.get("filter","filterpath") , targetpath)
    filterpath = targetpath

    # # change used filter in config
    # poeconfig = configparser.ConfigParser()
    # poeconfig.read(os.path.join(poedir, "production_Config.ini"), 
    #                encoding='utf-8-sig')
    # poeconfig.set("UI", "item_filter", filtername)

    # logging.info("Writing new filter to config.")
    # # writing filter to file
    # with open(os.path.join(poedir, "production_Config.ini"), 'w') as configfile:
    # # with open("production_Config.ini", 'w') as configfile:
    #     poeconfig.write(configfile)


if not os.path.isfile(filterpath):
    logging.info("File at filterpath does not exist, trying to find it anyways.")

    # get currently used filter from "production.ini" at %USERPROFILE%
    poedir = os.environ["userprofile"] + "\Documents\My Games\Path of Exile\\"
    poeconfig = configparser.ConfigParser()
    poeconfig.read(os.path.join(poedir, "production_Config.ini"), 
                   encoding='utf-8-sig')
    filtername = poeconfig.get("UI", "item_filter")

    # as the folder of the filter is not specified (as far as I know), just search for all files in poedir
    # (assuming the filter name is unqiue)
    paths = glob.glob(poedir + "**\\" + filtername, recursive=True)
    if len(paths) == 0:
        logging.warn("Could not find the filter, please check your settings.")
        raise FileNotFoundError
    elif len(paths) > 1:
        logging.warn("Found multiple filter with the same name, chosing the first and possibly wrong one.")
        filterpath = paths[0]
    else:
        filterpath = paths[0]


# main method
def repeat():
    logging.info("Requesting contents of stash tab(s).")
    resp = requests.get(url, params=payload, cookies=cookies)
    logging.info(f"GET request returned status_code {resp.status_code}.")
    resp = resp.json()

    itemcount = {}
    for name in itembases:
        itemcount[name] = 0

    for item in resp["items"]:
        if item["ilvl"] >= 60 and item["ilvl"] <= 74:
            itembase = item["typeLine"]
            
            # get item class
            for name in itembases:
                if itembase in itembases[name]:
                    itemcount[name] += 1
                    break
    logging.info(f"Found the following items: {itemcount}")
    
    counts = [itemcount[k] for k in itemcount if k != "rings"]
    counts.append(int(itemcount["rings"]/2))
    logging.info(f"Complete sets: {min(counts)}.")

    str_to_filter = ""

    # check if engough items are in tab
    item_threshold = config.getint("filter", "num_item_thresh")
    for name in itemcount:
        if itemcount[name] < item_threshold:
            str_to_filter += filteradds[name]
        if config.getboolean("filter", "always_highlight_jewellery") \
                and name in ["rings", "amulets", "belts"]:
            if filteradds[name] in str_to_filter:
                str_to_filter = str_to_filter.replace(filteradds[name], filteradds[name].replace("<= 74", "<= 100"))
            else:
                str_to_filter += filteradds[name].replace("<= 74", "<= 100")
    
    # check again for rings as you need two for each recipe, do the same for weapons as only 1h weapons are selected
    if itemcount["rings"] >= item_threshold and itemcount["rings"] < item_threshold*2 \
            and not config.getboolean("filter", "always_highlight_jewellery"):
        str_to_filter += filteradds["rings"]
    if itemcount["weapons"] >= item_threshold and itemcount["weapons"] < item_threshold*2:
        str_to_filter += filteradds["weapons"]
        
    str_to_filter += "\n" + split_helper
    logging.info("Created string for filter.")

    # check if change needed and write accordingly
    with open(filterpath, 'r+') as f:
        content = f.read()
        
        parts = content.split(split_helper)
        if parts[0] + split_helper == str_to_filter:
            logging.info("Filter is still up-to-date, no change.")
        else:
            logging.info("Filter is outdated, writing new filterinfo to file.")
            f.seek(0, 0)
            f.write(str_to_filter + parts[-1])
            f.close()
            if config.getboolean("settings", "toast_alert"):
                toaster.show_toast("Updated Filter!","Dont forget to refresh the filter on the options menu.", duration=3, icon_path="chaos.ico")


interval = config.getint("settings", "update_interval")
starttime = time.time()
loop = True
error_count = 0
while loop:
    try:
        repeat()
        error_count = max(error_count-1, 0) #error decay
    except Exception as e:
        error_count += 1
        logging.error(f"Exception encountered, {str(e)}.")
        logging.error(traceback.format_exc())
    if error_count >= 3:
        loop = False
        logging.critical(f"Ending loop, too many errors in recent runs ({error_count}).")
    else:
        time.sleep(interval - ((time.time() - starttime) % interval))