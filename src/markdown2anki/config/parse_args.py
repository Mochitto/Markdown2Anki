import logging
import argparse

from markdown2anki.utils.debug_tools import expressive_debug

logger = logging.getLogger(__name__)

# TODO: change me to the real docs
DOCS_URL = "www.google.com"

# Custom formatter used to preserve newlines in help messages
# https://stackoverflow.com/a/22157136/19144535
class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith("R|"):
            return text[2:].splitlines()

        return argparse.HelpFormatter._split_lines(self, text, width)


CommandLineArgsParser = argparse.ArgumentParser(
    prog="Markdown to Anki 🌸",
    description="Create your anki cards in markdown and enjoy them on Anki!\n"
    + "\n!Notice: when some arguments are not used, the corresponding option set in the config file "
    + "is used as a default.",
    epilog=f"For more information, visit: {DOCS_URL} to read the documentation! 🐙",
    # I ignore None values so that there is no "can't be empty" error
    # When validating the cli_arguments
    argument_default=argparse.SUPPRESS,
    formatter_class=SmartFormatter,
)

# Notice: "dest" is the same as how it's defined in the config.ini
# This is to "merge" the config file and the args using the same keys

# I/O operations
CommandLineArgsParser.add_argument(
    "-hc",
    "--healconfig",
    dest="Heal config?",
    help="R|If present, heals a broken configuration file.\n" + "Example: --healconfig",
    action="store_true",
    default=None,
)

CommandLineArgsParser.add_argument(
    "-apkg",
    "--AnkiPackage",
    dest="Anki package?",
    help="R|If present, re-builds the anki apkg file that you can import to your Anki to get the Markdown2Anki note types.\nExample: --apkg",
    action="store_true",
    default=None,
    )

CommandLineArgsParser.add_argument(
    "-lc",
    "--linkconfig",
    dest="Link config?",
    help="R|If present, shows the welcome screen and allows you to link to an existing config file\n or to create a new one, if missing.\n"
    + "Example: --linkconfig",
    action="store_true",
    default=None,
)

CommandLineArgsParser.add_argument(
    "-bf",
    "--badfile",
    dest="Bad file as input?",
    help='R|If present, uses the bad file as input instead of using the "input md file", useful if you fix the bad cards in the same file where they are put.\n'
    + "Example: --badfile",
    action="store_true",
    default=False,
)

# I/O options
CommandLineArgsParser.add_argument(
    "-v",
    "--vault",
    dest="Obsidian valut name",
    metavar="'YOUR VAULT'",
    help="R|The name of the obsidian vault where the input file is from.\n"
    + "Example: -v 'My obsidian vault'",
)

CommandLineArgsParser.add_argument(
    "-f",
    "--inputfile",
    dest="input md file path",
    metavar="YOURFILE.MD",
    help="R|The path to your markdown input file. This could be inside of your Obsidian vault.\n"
    + "Example: -f myCodingCards.md",
)

CommandLineArgsParser.add_argument(
    "-si",
    "--searchimage",
    dest="search images folder",
    metavar="/ABSOLUTE/PATH/TO/FOLDER",
    help="This is where the program will look for images when they appear in your cards.\nIt also searches inside of subfolders."
    + "Example: -si /home/myImages",
)

# Behaviour
CommandLineArgsParser.add_argument(
    "-ff",
    "--fastforward",
    dest="fast forward?",
    metavar="False|True",
    help="R|Whether or not to continue processing cards when there is an error in them.\nWhen fast forwarding, cards with errors are skipped but can still be found in the bad cards file and be fixed.\nWhen not fast forwarding, you will be showed the card and asked if you want to continue or not.\n"
    + "Example: --fastforward true (OR) --ff false",
)
CommandLineArgsParser.add_argument(
    "-cif",
    "--clearinputfile",
    dest="clear file?",
    metavar="False|True",
    help="R|Turns on input file clearing: the input markdown file is cleared (emptied of its content) upon cards' creation.\n"
    + "Example: --clearinputfile true (OR) -cif false",
)
CommandLineArgsParser.add_argument(
    "-xd",
    "--excludedir",
    dest="folders to exclude",
    metavar="'LIST, OF, DIRS'",
    help="R|Folders names to exclude when looking for images, divided with commas.\n"
    + "Example: -xd 'diary, wallpapers, camera' (OR) -xd 'diary'",
)
CommandLineArgsParser.add_argument(
    "-ln",
    "--linenumbers",
    dest="line numbers?",
    metavar="True|False",
    help="R|Adds line numbers to code blocks.\n"
    + "Example: --linenumbers true (OR) --ln false",
)
