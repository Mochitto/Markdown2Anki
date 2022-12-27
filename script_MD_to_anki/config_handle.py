import configparser
import os
import datetime

# Built at run-time
CURRENT_DIR = os.getcwd()
CURRENT_TIME = datetime.datetime.now()

# From the config file
def append_base_path_if_relative(file_path: str):
    global BASE_PATH
    if not os.path.isabs(file_path):
        return os.path.join(BASE_PATH, file_path)
    return file_path

def append_outdir_if_relative(file_path:str):
    global OUT_FOLDER
    if not os.path.isabs(file_path):
        return os.path.join(OUT_FOLDER, file_path)
    return file_path

config = configparser.ConfigParser()
config.read('config.ini')

BASE_PATH = config["BASEPATH"]["base_path"]
if not BASE_PATH:
    BASE_PATH = CURRENT_DIR

MD_INPUT_FILE = append_base_path_if_relative(config["INFILES"]["md_input_file"])

OUT_FOLDER = append_base_path_if_relative(config["FOLDERS"]["out_folder"])

RESULT_FILE = append_outdir_if_relative(config["OUTFILES"]["anki_csv_file"])
BAD_CARDS_FILE = append_outdir_if_relative(config["OUTFILES"]["failed_cards_file"])
LOG_FILE = append_outdir_if_relative(config["OUTFILES"]["log_file"])

FAST_FORWARD = config["BEHAVIOR"]["fast_forward"]
LINENOS = config["BEHAVIOR"]["linenos"]

# Set-up
os.makedirs(OUT_FOLDER, exist_ok=True) # Build out folder if missing





