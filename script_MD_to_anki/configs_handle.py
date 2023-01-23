import configparser
import os
import re
import argparse
from typing import List
import logging

import md_2_anki.utils.card_types as Types
from md_2_anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)

# Refactor: There must be a better method to check for config file corruption 
# maybe have a special method that does a check on ALL of the options..? 

# TODO: Create default config file using code; that way it's also super easy to have
# a health check using the same structure.

# FIXME: None type doesn't work for os.path.isabs; there needs to be some type checking beforehand
# OR paths can be validated.

class ConfigError(Exception):
    """
    Used for errors while parsing the configurations.
    """
    pass

def get_config_file():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

class MergeConfigs:
    """
    This class is used to merge and validate configurations from
    the argparse and configparser.

    The result is merged_config, a dictionary having:
        key: option,
        value: value
    """
    def __init__(self, command_line_args: argparse.Namespace, config_from_file) -> None:
        self.merged_config = {}  

        self._cli_args = command_line_args
        self._file_config = config_from_file

        # Next proprieties are used for config validation.
        self._APPEND = [  # key: option from which path to append, value: options to check; order matters 
                        {"base_path": {"md_input_file", "out_folder"}},
                        {"out_folder": {"images_out_folder", "anki_csv_file", "clozes_anki_csv_file", "failed_cards_file", "log_file"}}, 
                    ]
        self._BOOL = {"fast_forward", "linenos", "show_config_in_log"}
        self._REQUIRED = {  # key: option, value: error message
            "vault_name": "Please specify a vault name.\n"+
                "!! If you don't make use of Obsidian, you can set this to any value.", 
            "images_dir": "Please specify a directory where to look for images.\n"+
                "!! If you don't make use of images in your notes, you can set this to any value."
                }
        self._EXISTS = {  # key: option, value: error message
            "md_input_file": "The specified input file doesn't exist.\n",
            "images_dir": "The specified images directory doesn't exist.\n",
            "base_path" : "The specified base path doesn't exist.\n"
                }
        
        self.__post_init__()


    def __post_init__(self) -> None:
        """
        Populate self.merged_config.
        """
        self._merge_configs()
        self._append_paths_to_merged_config()
        self._validate_merged_config()
        if self.merged_config.get("show_config_in_log", None):
            expressive_debug(logger, "Configuration", self.merged_config)
        print(self.merged_config)


    def _merge_configs(self) -> None:
        """
        Update self.merged_config with options from cli_args
        if they are present; else use the value from the config file.
        """
        config = self._file_config
        cli_config = vars(self._cli_args)
        for section in config.sections():
            for option, section_values in config.items(section):
                if option in cli_config and cli_config[option]:
                    self.merged_config[option] = cli_config[option]
                else:
                    self.merged_config[option] = section_values
    
    def _append_paths_to_merged_config(self) -> None:
        """
        Use self.APPEND (referring to its keys as key_option and values as options) to
        append the key_option's path (from self.merged_config) to the option's path, if relative. 
        """
        # FIXME PLEASE WHAT IS THIS STRUCTURE
        for pair in self._APPEND:
            for key_option, options in pair.items():
                for option in options:
                    try:
                        option_value = self.merged_config[option]
                        key_option_value = self.merged_config[key_option]
                        self.merged_config[option] = self._append_path_if_relative(key_option_value, option_value)
                    except KeyError:
                        # Option missing from config
                        self._log_corruption(option)

    def _append_path_if_relative(self, base_path: Types.PathString, file_path: Types.PathString) -> Types.PathString:
        """
        Append base_path if file_path is relative.
        """
        if not os.path.isabs(file_path):
            return os.path.join(base_path, file_path)
        return file_path

    def _validate_merged_config(self) -> None:
        """
        Check for errors in the configuration.
        If there is any, let the user know what the problem is
        and raise ConfigError.
        """
        try:
            errors = []
            # Error checking ----------
            # Check required options
            for required_option, error_message in self._REQUIRED.items():
                if not self.merged_config[required_option]: 
                    errors.append(error_message)
            
            # Check paths that should exist
            for option, error_message in self._EXISTS.items():
                option_path = self.merged_config[option]
                if not os.path.exists(option_path):
                    error_message += f"Path: {option_path}"
                    errors.append(error_message)

            if errors:
                logger.error("\n❌ CONFIG ERROR:".join(errors))
                raise ConfigError("One or more required options were left unset.")
            
            # Formatting -----------
            # Turn comma separated values to list
            folders_to_exclude =  self.merged_config["folders_to_exclude"]
            self.merged_config["folders_to_exclude"] = self._comma_string_to_list(folders_to_exclude)

            for option in self._BOOL:
                self.merged_config[option] = bool(self.merged_config[option])
                
            # Set-up -------------
            # If base_path is unset, use cwd
            if not self.merged_config["base_path"]:
                self.merged_config["base_path"] = os.getcwd()
            # Create folders if missing
            os.makedirs(self.merged_config["out_folder"], exist_ok=True)
            os.makedirs(self.merged_config["images_out_folder"], exist_ok=True)
        except KeyError as err:
            self._log_corruption(err.args[0])

    def _comma_string_to_list(self, str_list: str) -> List[str]:
        return re.split(r"\s*,\s*", str_list)
    
    def _log_corruption(self, option:str):
        logger.critical(f"Your config file is corrupted. MISSING OPTION: '{option}'\n"+
                        "Please create again the config file.")
        raise ConfigError("CRITICAL: corrupted config file.")


