import configparser
import os
import datetime

# Built at run-time
CURRENT_DIR = os.getcwd()
CURRENT_TIME = datetime.datetime.now()

# From the config file
config = configparser.ConfigParser()
config.read('config.ini')

BASE_PATH = config["BASEPATH"]["base_path"]
if not BASE_PATH:
    BASE_PATH = CURRENT_DIR

MD_INPUT_FILE = config["PATHS"]["md_input_file"]
OUT_FOLDER = config["PATHS"]["out_folder"]

# Set-up
os.makedirs(os.path.join(BASE_PATH, OUT_FOLDER), exist_ok=True) # Build out folder if missing

def append_base_path_if_relative(config_path: str):
    if not os.path.isabs(config_path):
        
