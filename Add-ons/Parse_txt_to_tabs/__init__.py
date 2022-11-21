from aqt import mw, editor
from aqt.qt import QDialog, QGridLayout, QPushButton, QLabel
from anki.hooks import addHook, remHook, runHook

from functools import partial
import re
import sys

from . import definitionGetter

# stores the entries that need to be added when dialogs end
finalEntries = []
first = True
config = mw.addonManager.getConfig(__name__)

# adds the selected dictionary entry and closes dialog
def buttonPressed(entry,window):
    global finalEntries
    finalEntries.append(entry)
    window.close()

def getBoldWords(html):
    matches = re.findall(r'.+',html)
    # FIXME - Fix for multiple, bold words functioning
    # if len(matches) > 1:
    #     matches = re.findall(r'<b>(.+?)</b>',html) 
    return matches

def getNoteType(name):
    global config
    for notetype in config['notetypes']:
        if(name == notetype['name']): 
            return notetype
    return None

def correctOrder(flag, n, fidx):
    global first
    first = False
    remHook('editFocusLost', theMagic)
    runHook('editFocusLost',flag,n,fidx)
    addHook('editFocusLost', theMagic)

def getActiveWindow(note):
    for widget in mw.app.allWidgets():
        # finds the editor in use
        if isinstance(widget, editor.EditorWebView) and widget.editor.note is note:
            return widget
    return None

# FIXME - fix for multiple bold words (Line 23)
# def getDefinitionChoiceDialog(aw, entries):
#     d = QDialog(aw)
#     grid = QGridLayout()

#     # adds found definitions to dialog window
#     for x in range(len(entries)):
#         button = QPushButton(entries[x].word)
#         button.clicked.connect(partial(buttonPressed, entries[x],d))
#         label = QLabel()
#         label.setText(entries[x].shortDef)
#         label.setWordWrap(True)
#         grid.addWidget(button,x,0)
#         grid.addWidget(label,x,1,1,5)
#     d.setLayout(grid)
#     return d


def theMagic(flag, n, fidx):
    global finalEntries, first, config
    fields = mw.col.models.fieldNames(n.model())
    notetype = getNoteType(n.model()['name'])
    sys.stdout.write("|||".join(fields))
    if not notetype:
        # not a notetype that has the add-on enabled, don't do anything
        return flag

    if fields[fidx] != notetype["src"]:
        # not the src field that has been edited, don't do anything
        return flag
    src = fields[fidx]
    dst = notetype["dst"]

    if not dst:
        raise ValueError("The dst and src fields in config don't match those on the card")
    
    try:
        if n[dst]:
            # dst isn't empty, to avoid overwriting data, don't do anything
            return flag
    except KeyError: # Avoid crashing if the user adds a Note type that had the source but not the destination
        return flag

    aw = getActiveWindow(n)
    if not aw:
        return flag
    
    # because this add-on loads first and it reacts with the reading generator strangely, gotta put it in the back
    if first:
        correctOrder(flag, n, fidx)
    
    boldWords = getBoldWords(n[src])
    # runs the dialogs
    # Mochitto's comments vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    # FIXME - fix me for multiple words
    for word in boldWords:
        entries = definitionGetter.parseSearch(word)
        finalEntries.append(entries[0])

    # puts the output into the note and saves
    output = ""
    # FIXME - fix me for multiple words
    for entry in finalEntries:
        output += f"<div class='jisho-div'>\n{entry}\n</div>"
    n[dst] = output
    try:
        n.to_backend_note()
    except AttributeError:
        if not aw.editor.addMode: 
            n.flush()
    aw.editor.loadNote(focusTo=fidx+1)
    finalEntries = []

    # prevents focus from advancing and messing the edits up
    return False

# tells anki to call theMagic when focus is lost (you move out of a text field or something)
addHook('editFocusLost', theMagic)
