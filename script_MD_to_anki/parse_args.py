import logging
import argparse
import sys

from md_2_anki.utils import expressive_debug

logger = logging.getLogger(__name__)

DOCS_URL = "www.google.com"

# Custom formatter used to preserve newlines in help messages
# https://stackoverflow.com/a/22157136/19144535
class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()  

        return argparse.HelpFormatter._split_lines(self, text, width)

CommandLineArgsParser = argparse.ArgumentParser(
        prog="Markdown to Anki 🌸",
        description="Create your anki cards in markdown and enjoy them on Anki!\n" +
        "\n!Notice: when some arguments are not used, the corresponding option set in the config file " +
        "is used as a default.",
        epilog=f"For more information, visit: {DOCS_URL} to read the documentation! 🐙",
        formatter_class=SmartFormatter
        )

# Notice: "dest" is the same as how it's defined in the config.ini
# This is to "merge" the config file and the args using the same keys
CommandLineArgsParser.add_argument("-f", "--inputfile",
                    dest="md_input_file",
                    metavar="YOURFILE.MD",
                    help="R|The markdown file to parse into anki cards.\n" +
                    "Example: -f myCodingCards.md"
                    )
CommandLineArgsParser.add_argument("-v", "--vault",
                    dest="vault_name",
                    metavar="'YOUR VAULT'",
                    help="R|The name of the obsidian vault where the input file is from.\n"+
                    "Example: -v 'My obsidian vault'")
CommandLineArgsParser.add_argument("-ff", "--fastforward",
                    dest="fast_forward",
                    help="R|Turns fast forward mode on (continue even if there is an error with a card)\n"+
                    "Example: -ff",
                    action='store_true'
                    )
CommandLineArgsParser.add_argument("-id", "--imagedir",
                    dest="images_dir",
                    metavar="/ABSOLUTE/PATH/TO/THE/DIR",
                    help="R|Absolute path: where to recursively look for images when they are found in your markdown.\n"+
                    "Example: -id /home/me/MyVault/images",
                    )
CommandLineArgsParser.add_argument("-xd", "--excludedir",
                    dest="folders_to_exclude",
                    metavar="'LIST, OF, DIRS'",
                    help="R|Folders names to exclude when looking for images, divided with commas.\n"+
                    "Example: -xd 'diary, wallpapers, camera' (OR) -xd diary"
                    )
CommandLineArgsParser.add_argument("-of", "--outfolder",
                    dest="out_folder",
                    metavar="/ABSOLUTE/PATH/TO/THE/DIR",
                    help="R|Absolute path: where the resulting files are put, if their path is relative.\n"+
                    "Example: -of /home/me/ankiFiles"
                    )
CommandLineArgsParser.add_argument("-ln", "--linenos",
                    dest="linenos",
                    help="R|Adds line numbers to code blocks\n"+
                    "Example: -ln"
        )

