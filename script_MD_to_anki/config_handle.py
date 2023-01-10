import configparser
import datetime
import os

import card_types as Types

# Built at run-time
CURRENT_DIR = os.getcwd()
CURRENT_TIME = datetime.datetime.now()


# From the config file
def append_path_if_relative(base_path: Types.PathString, file_path: Types.PathString) -> Types.PathString:
    if not os.path.isabs(file_path):
        return os.path.join(base_path, file_path)
    return file_path


config = configparser.ConfigParser()
config.read("config.ini")

BASE_PATH = config["BASEPATH"]["base_path"]
if not BASE_PATH:
    BASE_PATH = CURRENT_DIR

# Append BASE_PATH if relative
MD_INPUT_FILE = append_path_if_relative(BASE_PATH, config["INFILES"]["md_input_file"])
OUT_FOLDER = append_path_if_relative(BASE_PATH, config["FOLDERS"]["out_folder"])

# Append OUT_FOLDER if relative
RESULT_FILE = append_path_if_relative(OUT_FOLDER, config["OUTFILES"]["anki_csv_file"])
CLOZES_RESULT_FILE = append_path_if_relative(OUT_FOLDER, config["OUTFILES"]["clozes_anki_csv_file"])
BAD_CARDS_FILE = append_path_if_relative(OUT_FOLDER, config["OUTFILES"]["failed_cards_file"])
LOG_FILE = append_path_if_relative(OUT_FOLDER, config["OUTFILES"]["log_file"])

FAST_FORWARD = bool(config["BEHAVIOR"]["fast_forward"])
LINENOS = bool(config["BEHAVIOR"]["linenos"])

# TODO: validate these variables to make sure they are configured
VAULT = config["NECESSARY"]["vault_name"]

# Set-up
os.makedirs(OUT_FOLDER, exist_ok=True)  # Build out folder if missing
