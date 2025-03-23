## Importing your cards via CSV - Legacy feature

<!-- prettier-ignore -->
> ![NOTE]
> This feature is considered legacy. Currently, the recommended way to import
> cards is via AnkiConnect plugin. To use this feature, you need to set `"use legacy CVS output?"` 
> option in .ini config file to `True`.

### Importing your cards

Once you have processed your cards, they will be divided in cards with clozes
and cards without clozes. Those will become two `.csv` files:
`basic_anki_cards.csv` and `clozed_anki_cards.csv`. To import these, you have to
open up Anki and press the "Import File" in the lower side of the main menu, or,
if you prefer, you can use "File>Import" from the menu in the top-left of the
Anki app. After selecting the `.csv` file, you have to let anki know that the
separator used is `Comma`, select the right `note type` and the deck you wish
the cards to be imported in. Also make sure to allow HTML in the cards, as they
need it to work correctly.

This is a screenshot of how this could look in your Anki (Anki's UI can change
depending on the OS it is running on):
![Image of Anki's import screen](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Anki_import_example.webp)

You can find more information on importing to Anki here:
https://docs.ankiweb.net/importing.html

### Importing your images

You can import images automatically if you add the path to your
[Anki media folder](https://docs.ankiweb.net/files.html#file-locations) in the
config file. Images that are already present won't be added twice and will be
skipped (based on filename). If you prefer checking the images before importing
them manually, you can point to another folder or leave the default one.
**Notice:** when images are copied, they lose their metadata: this is due to
security, as others' could read your images metadata if you were to share your
cards, and for how the python library that handles the copying process is
implemented.
