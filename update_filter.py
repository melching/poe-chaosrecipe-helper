import datetime, time
import requests
import os

import configparser
import logging
import traceback

from win10toast import ToastNotifier
import six
import appdirs
import packaging.requirements

from itembases import *

import ctypes


# load config from file
config = configparser.ConfigParser()
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


# create dict to map relevant bases to item class
bases = {
    "rings": ring_bases,
    "amulets": amulet_bases,
    "belts": belt_bases,
    "body_armours": body_bases,
    "gloves": glove_bases,
    "boots": boot_bases,
    "helmets": helmet_bases,
    "weapons": claw_bases + dagger_bases + wand_bases + sword_bases
}

# define strings for filter, customizable for each object
head = "Show # ChaosRecipeMod\n"
tail = "\n\
    ItemLevel <= 74\n\
    ItemLevel >= 60\n\
    PlayAlertSound 16 300\n\
    Identified False\n\
    HasInfluence None\n\
    Rarity Rare\n\
    SetFontSize 30\n\
    SetBorderColor 0 0 0 255\n\
    SetBackgroundColor 200 0 0 255\n\
    MinimapIcon 2 Orange Kite\n\n"

str_ring =    head + "    Class Ring" + tail
str_amulet =  head + "    Class Amulet" + tail
str_belt =    head + "    Class Belt" + tail
str_glove =   head + "    Class Glove" + tail
str_boot =    head + "    Class Boot" + tail
str_body =    head + "    Class \"Body Armours\"" + tail
str_helmet =  head + "    Class Helmet" + tail
str_weapon1 = head + "    Class \"Claws\" \"Daggers\" \"Wands\"" + tail
str_weapon2 = head + "\
    Class Sword\n\
    Width < 2\n\
    Height < 4\
" + tail

filter_strings = {
    "rings": str_ring,
    "amulets": str_amulet,
    "belts": str_belt,
    "body_armours": str_body,
    "gloves": str_glove,
    "boots": str_boot,
    "helmets": str_helmet,
    "weapons": str_weapon1+str_weapon2
}


# just a string to help split the filter
split_helper = "#imjustalinetohelptosplitthefileproperlyjustignoreme"

if config.getboolean("settings", "toast_alert"):
    logging.info("Creating ToastNotifier")
    toaster = ToastNotifier()


# main method
def repeat():
    logging.info("Requesting contents of stash tab(s).")
    resp = requests.get(url, params=payload, cookies=cookies)
    logging.info(f"GET request returned status_code {resp.status_code}.")
    resp = resp.json()

    itemcount = {}
    for name in bases:
        itemcount[name] = 0

    for item in resp["items"]:
        if item["ilvl"] >= 60 and item["ilvl"] <= 74:
            itembase = item["typeLine"]
            
            # get item class
            for name in bases:
                if itembase in bases[name]:
                    itemcount[name] += 1
                    break
    logging.info(f"Found the following items: {itemcount}")
    
    counts = [itemcount[k] for k in itemcount if k != "rings"]
    counts.append(int(itemcount["rings"]/2))
    logging.info(f"Complete sets: {min(counts)}.")

    str_to_filter = ""

    # check if engough items are in tab
    item_threshold = config.getint("poeinfo", "num_item_thresh")
    for name in itemcount:
        if itemcount[name] < item_threshold:
            str_to_filter += filter_strings[name]
    
    # check again for rings as you need two for each recipe
    if itemcount["rings"] >= item_threshold and itemcount["rings"] < item_threshold*2:
        str_to_filter += filter_strings["rings"]
        
    str_to_filter += "\n" + split_helper
    logging.info("Created string for filter.")

    # check if change needed and write accordingly
    with open(config.get("settings", "filterpath"), 'r+') as f:
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