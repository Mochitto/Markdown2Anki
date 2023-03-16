# Markdown2Anki
Markdown2Anki is a Python script that allows you to easily format your cards using Markdown syntax, and then import them into Anki while retaining the structure you gave them.  
This tool supports code highlighting, clozes, and images, making it a versatile and convenient option for anyone looking to streamline their flashcard creation process.
Additionally, it offers support for Obsidian notes, allowing you to create links inside your cards that point to your vault's notes! 🌸

---
![Demo image](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Main-demo_1.webp) 
> Unleash the power of spaced repetition: Convert your Markdown notes into Anki flashcards for optimal learning.  
`ChatGPT, when asked for a captivating description of this project.`

---
## Table of contents (for GitHub)
- [Features](#features)
  - [Technical features](#technical-features)
  - [Images](#images)
- [Installation](#installation)
  - [Initial setup](#initial-setup)
  - [Using fill the blanks](#using-fill-the-blanks)
- [Usage](#usage)
  - [Markdown formatting](#markdown-input-formatting)
  - [Importing cards](#importing-your-cards)
  - [Importing images](#importing-your-images)
  - [Errors and Bad cards](#errors-and-bad-cards)
  - [Using clozes](#using-clozes)
  - [Changing themes](#changing-themes)
  - [Navigating the UI](#navigating-the-ui)
- ["Can't find any element..." query Error](#query_error)
- [Creating a custom theme](#creating-a-new-theme)
- [Contributing and dev documentation](#contributing-and-dev-documentation)
- [The reasons behind the project](#the-reasons-behind-the-project)
- [Technologies used](#technologies-used)
- [Hopes for the future](#hopes-for-the-future)
- [Versioning](#versioning)
- [License](#license)
- [Closing note](#closing-note)

---
This is an open-source free software, you can find it on:  
Github - https://github.com/Mochitto/Markdown2Anki  
PyPi - https://pypi.org/project/markdown2anki

---

## Features
- **Write and format cards in Markdown**: create cards in Markdown syntax and then import them into Anki while retaining their structure.
- **Custom Note types** that support split-screen, tabs, keyboard shortcuts, and mobile devices.
- **No addons needed**: The resulting cards are pure HTML and the note-type is CSS and JS, which work with vanilla Anki.
- **Different themes**: themes for both day and night modes, which are easily customizable. You can [check them out here](https://github.com/Mochitto/Markdown2Anki/tree/master/themes)!
- **Code highlighting** (using [pygments](https://pygments.org/)).
- **Support for clozes** including those in code blocks.
- **Support for images** with automatic importing: the program can find the images you mention in your obsidian notes and copy them to your Anki's media folder.
- **Support for Obsidian links and images**: using `[[Note.md|my Note]]` and `[[my_image.jpg]]`-like markdown.
- **Accessible config file** that can self-heal (using [Type-Config](https://pypi.org/project/type-config/)): retaining as many custom configurations as possible even if the file is corrupted. This also ensures that if options are added with updates, your custom configuration will be retained.
- **Helpful error messages and feedback**.
- **Backup files of your inputs**, to help you retry in case something goes wrong.
- **Funny and expressive emoji in the CLI** to make the tool more engaging and enjoyable to use.
### Technical features
- **Extensive python tests coverage**: as of 2023-03-13, there are 108 tests for this tool to ensure its robustness and reliability.
- **Modular structure** to facilitate maintainability and contributions.
- **Os agnostic**: this tool can run on any operating system.
- **Type-safe python and javascript**.
- **Type-safe user configuration**: user configurations are validated and type-casted upon file-reading to ensure their accuracy and consistency.
- **SMACSS methodology driven SASS/CSS, with BEM classes nomenclature**: for organized and structured styling.
- **Minified and bundled JS/CSS** including themes, for efficient and fast performance in the "production" note type.
- **Mobile first responsive CSS**: to ensure it's fully responsive on all devices.
- **High-level dev documentation** to make it easier for contributions and maintenance.

## Images

### CLI
![Demo image of the CLI](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Terminal-demo.webp)  
![Video demo of the CLI](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/CLI_demo.mp4)
### Split-screen
![Demo image](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Demo-split-screen.webp) 
### Code highlighting
![Demo code highlighting](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Demo_highlight.gif)
### Clozes support
![Demo image](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Demo-cloze-standard.webp) 
![Demo image](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Demo-cloze-answer.webp) 
### Supports the addon "fill the blanks"
![Demo image](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Usage_demo1.webp)
### Mobile (with light mode)
Mobile version | Clozes in mobile
:---: | :---:
![Demo image of mobile](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/mobile_demo.webp) | ![Demo image of mobile](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/mobile_cloze_demo.webp)

## Installation

This project is distributed using `pip` via [Pypi](https://pypi.org/).
This means you need Python installed on your machine, you can get it here: https://www.python.org/downloads/  
**IMPORTANT!**: When installing, make sure to check the `Add python to PATH` if on Windows/Mac.

Once you have installed Python, you can write in the command line:
```bash
python -m pip install Markdown2Anki
```
And then you should be able to run:
```bash
md2anki
```
There is a guided setup on your first time running the app, which will help you get up and running :)  


**Notice:** This app uses emoji to give instant feedback to the user, depending on your terminal you might not be able to see them correctly.  
On windows you can use the [Windows terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701). 
On iOS and Linux they should be supported by default.

You can also get all of the possible arguments for the script with:
```bash
md2anki -h
```

The script will also let you know when there is a new update and point you to the [CHANGELOG.md](https://github.com/Mochitto/Markdown2Anki/blob/master/CHANGELOG.md) file, where you can read what has changed and decide if to update or not.  
![Update demo](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Demo-update.webp)
You can update the package with:
```bash
python -m pip install --upgrade Markdown2Anki
```
After doing this, the app will ask you again the location of your program folder and update (or heal) your configuration if it is present; if not, it will create a new one.

### Initial setup
During the initial setup process, you will be prompted to select a folder where the program will put its files.  
Once you will have confirmed the path to said folder, a configuration file named `md2anki.config.ini` will be added to it.  
The configuration file holds all the information on each option, what it does and if it's required or not.

**Suggested:** Among the options, you might want to set as `images out-folder` your Anki media folder; this option sets the folder where images are copied to when they are found in your notes; by setting it to your anki's media folder, images are automatically added to you Anki's database.  
You can learn more about Anki's folders here: https://docs.ankiweb.net/files.html#file-locations

There will also be a `markdown2anki.apkg` file which contains the anki note types you will need when importing the cards.  
If you have Anki installed on your system, you should be able to just double-click the file to import it, and it will create a new deck with some template cards and the note types.  
You can learn more on `.apkg` files here: https://docs.ankiweb.net/exporting.html#deck-apkg

### Using fill the blanks

If you would like to have "type-in" clozes, you can use this addon: [fill the blanks addon](https://ankiweb.net/shared/info/1933645497).  
For it to work, you will need to duplicate the `Markdown2Anki - Cloze` Note type and modify it by changing the `Front side` field to: `{{type:cloze:Front}}`.  

This is a video with how you can achieve this: ![Video Tutorial on how to modify a note type](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/How_to_make_type_in_cloze.mp4)

![Demo of fill the blanks](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Demo-cloze-addon.webp)

## Usage

### Markdown input formatting
To ensure that your notes are properly recognized by the program, there are a few formatting requirements:

#### Cards separator
Cards must be separated by a horizontal rule using three dashes or more `---`.  
**Notice:** `***` do not work as cards separators, this is so that you can use `*` to define horizontal rules inside of your cards :)

#### Tabs
A unique feature of this program is the ability to create tabs within your cards.  
Tabs are divided depending on the card side (front, back) and the tabs side (left window, right window).  

Front side tabs, unless removed with the `-` flag (more on this later), are retained when moving to the back side (aka. "flipping the card").  
Back side tabs are added after the front tabs, unless they replace one that has been removed.

#### Tab Labels and flags
Tab labels define the beginning of a tab and its content, and should be formatted as follows:
```
## <flags> [<tab label>]
```

Flags define where your tab goes (left or right side of the card, front or back side of the card).  

The possible flags are:
Flags | Meaning 
 --- | --- 
`F` | Front side of the card
`B` | Back side of the card 
`L` | Left tabs side
`R` | Right tabs side
`-` | Only applied to Front tabs: removes the tab when switching to the back side
`+` | Only applied to Back tabs: replaces a removed front tab 

```markdown
## BR [This is my tab]
And this is its body
```
**Notice:** Tab labels do not support Markdown formatting, such as bold text etc.

**Default values**:  
`F`ront and `L`eft flags are applied automatically, so you can leave them out.
```markdown
## [My tab]
is the same as
## FL [My tab]

## B [My tab]
is the same as 
## BL [My tab]

## R [My tab]
is the same as
## FR [My tab]
```

#### Example
Here are two example cards to illustrate the formatting requirements:
```markdown
## - [Question]
# A great addition to humanity
What is the **name** of this funny cat?
## Make sure you get it right.

## R [Funny cat]
![[bingus.png]]

## +B [Answer]
This is the magnificent Bingus.

---

## [Complete the code]
This is the code needed to reverse sort a list.
```python
my_list = [3,5,2]
# New list
sorted_list = {{C1::sorted}}(my_list, {{C1::True}})
# In place
my_list.{{C1::sort}}(True)
    ```

```
The result:
![Usage demo image 2](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Usage_demo2.webp)
![Usage demo image 3](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Usage_demo3.webp)
(This is using the [fill the blanks addon](https://ankiweb.net/shared/info/1933645497))
![Usage demo image 1](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Usage_demo1.webp)

### Importing your cards
Once you have processed your cards, they will be divided in cards with clozes and cards without clozes.  
Those will become two `.csv` files: `basic_anki_cards.csv` and `clozed_anki_cards.csv`.  
To import these, you have to open up Anki and press the "Import File" in the lower side of the main menu, or, if you prefer, you can use "File>Import" from the menu in the top-left of the Anki app.  
After selecting the `.csv` file, you have to let anki know that the separator used is `Comma`, select the right `note type` and the deck you wish the cards to be imported in.
Also make sure to allow HTML in the cards, as they need it to work correctly.

This is a screenshot of how this could look in your Anki (Anki's UI can change depending on the OS it is running on):  
![Image of Anki's import screen](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Anki_import_example.webp)

You can find more information on importing to Anki here: https://docs.ankiweb.net/importing.html

### Importing your images
You can import images automatically if you add the path to your [Anki media folder](https://docs.ankiweb.net/files.html#file-locations) in the config file.  
Images that are already present won't be added twice and will be skipped (based on filename).  
If you prefer checking the images before importing them manually, you can point to another folder or leave the default one.   
**Notice:** when images are copied, they lose their metadata: this is due to security, as others' could read your images metadata if you were to share your cards, and for how the python library that handles the copying process is implemented.

Hopefully, in the near future, the importing part will be made automatic by the addition of `AnkiConnect` support.

### Errors and Bad cards
When there are errors in formatting, the app will let you know what went wrong and create a `Bad_cards.md` file in your program folder.  
This will be a file of all of the "Bad cards" (cards that had a problem in them). The specific error for each card is added before the tabs, so that you can easily fix them.

These, as other text added at the beginning of a card, before all the tabs labels, are considered comments, so you can leave them in.  
For example:
```markdown
❌ ERROR ❌ - A card without front tabs has been found.
## B [My card]
That is very cool ⭐

---

❌ ERROR ❌ - A tab without body has been found.
## [Fast inverse square root]
```

Some common card errors are:
- Forgetting the body of a tab
- Leaving the front-side of a card empty
- Removing a tab that contains a cloze in it  

Some common general errors are:
- The configuration file is missing a necessary option (such as your `vault's name`)
- No cards were found in the input file


Once you have fixed your bad cards, you can run the program with 
```
md2anki -bf
```
This will automatically use the `Bad_cards.md` as input, if you prefer fixing the cards in that file instead of adding them to the main input file.

A `debug_log.txt` file is also present in your program folder, which is created every time you run the program. This file contains more information on what happens when the program is running, the result of various processes, your configuration and so on.  
If you find a bug in the program, it would be of great help if you could add this file to your issues on GitHub.  

**Privacy Notice:** the log file has your configuration in it, as it can contain crucial information for debugging.  
If you don't want to share your paths or other information from it when making issues, you should search-and-replace that information with some fake one, while trying not to change their general structure.

### Using clozes
You can specify clozes in your markdown and they will be carried over to your anki cards. Whenever there is a word or sentence you'd like to have as a cloze, you can use Anki's formatting `{{c<number>::<word>}}` (notice the two colons, not just one).

The number tells Anki what cloze to add to what card. This means that if you have C1, C2 and C3, there will be three cards created (this is a feature of Anki, not of Markdown2Anki), each missing the respective words.  
More on this here: https://docs.ankiweb.net/editing.html#cloze-deletion

If the clozed word/sentence is present multiple times, it will be automatically turned into a cloze, so you only need to specify it once.
This works also in code blocks.

For example:
```python
my_list = [3,5,2]
# New list
sorted_list = {{C1::sorted}}(my_list, {{C1::True}}) 
# In place
my_list.{{C1::sort}}(True)
```
Result
Notice how all instances of `sort` and `True` are turned into clozes, even if only specified once in the Markdown text.
![Demo of clozes](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/cloze_example.webp)

### Changing Themes
The default theme is mochitto's Rosé Pine theme, but there is also a catpuccin theme.  
You can find all the themes in the [themes folder](https://github.com/Mochitto/Markdown2Anki/tree/master/themes).  
To use another theme, you can just copy the CSS from the file in the themes folder and paste it in your Note types' styling field.  

This can be found by accessing `Tools>Manage Note Types>(select your note type)>Cards(on the right)>Styling(on the left)`. The `Tools` menu is found in the top-left part of Anki's main menu.   
You can reference this: ![Video Tutorial showing how to access a card's style](https://github.com/Mochitto/Markdown2Anki/blob/master/docs/How_to_find_styling.mp4)

You can read more on how styling happens here: https://docs.ankiweb.net/templates/styling.html

### Navigating the UI
The custom User Interface of the note-type that comes with this project is focused on the concept of tabs.  
You can have side-by-side tabs and multiple tabs to toggle through.  

![Demo image](https://raw.githubusercontent.com/Mochitto/Markdown2Anki/master/docs/Main-demo_1.webp)

To navigate them, you can either click on the labels of non-active tabs to make them active (switch to them), and click an active tab to make it full-screen.  
This works also in mobile. 

There are also keyboard commands: you can select a tab with `<alt>+<number of the tab>` or `⌥  + <number of the tab>` (the number is displayed next to the tab label) to switch to that tab or make it full-screen, or you can `TAB` between to navigate between them.  

For example, `Alt+1` will show the first tab if it's not-active, or make it full-screen if it's active.

**Notice**: at times the hotkeys don't seem to work completely (maybe one tab is not accessible with `<alt>`); I'm working on understanding better how Anki handles HTML and Javascript, as it's a problem on how it handles changing between cards... The `<tab>` and `<click>` methods seem to be stable, so you can use those if this bug happens.  
I'm sorry about it...

## Query error
Sometimes, you might come across a screen saying "ERROR: Couldn't find any element using the query [...]".  
This happens because, for some reason, Anki is not loading correctly the card or the script. This shouldn't happen often and I'm still trying to understand better the underlying reasons behind it, as they have to do with Anki's way of handling HTML and Javascript...  
It will likely be patched in the near future, until then, your best call is to go back to the main menu and try again, or restarting Anki; this often fixes the problem.  
I'm sorry about it...

## Creating a new theme
The theme was made with customizability in mind; you can learn more on how to make your own theme in the [theme builder folder's README](https://github.com/Mochitto/Markdown2Anki/tree/master/theme_builder).  
Once you've made your own theme, you can submit it as a contribution to make it "official" and share it with others.

## Contributing and dev documentation
The project was built with contributions and future projects in mind, using expressive names, doc strings on functions/classes/modules and types.  
You can read more on the project's inner workings in the [CONTRIBUTING.md](https://github.com/Mochitto/Markdown2Anki/blob/master/CONTRIBUTING.md).  
If you want to help with issues, you can head to [this project's kanban](https://github.com/users/Mochitto/projects/3).

If you have any questions or find something in the documentation that is not clear, let me know with an issue, I'll (mochitto) will get back to you asap!

## The reasons behind the project
Anki uses formatted text and html, but makes users pick a very strict way of defining that, while using plain text.
This "helps" some users by shielding them from the possible complexity of formatting the text, but a lot more could be achieved by giving them freedom with Markdown.  

Markdown formatting also makes space for coding cards, which are pretty awful to make in Anki (even if, thanks to [Ijgnd](https://ankiweb.net/shared/info/1100811177) and [Glutanimate](https://ankiweb.net/shared/info/1463041493), there was at least an ok possibility to make them work).  
This means that users do not really need tens of note types, but can define the kind of note they actually need while writing them (or by using their own, flexible templates).  
This also takes away some limitations, such as having to use clozes on only one field of the card.

I (mochitto) also really like the idea of Open Source/Free software communicating between different projects, so creating a "bridge" between Obsidian and Anki feels like a great way of pulling together applications that give society a huge value, making them even stronger.

## Technologies used
### Languages
- [Typescript](https://www.typescriptlang.org/)
- [Sass](https://sass-lang.com/)
- [Python](https://www.python.org/)
### Building
- [Esbuild](https://esbuild.github.io/)
- [Esbuild sass plugin](https://www.npmjs.com/package/esbuild-sass-plugin)
- [Live server](https://www.npmjs.com/package/live-server) 
### Core dependencies
- Markdown to HTML parser and compiler: [Mistune](https://mistune.lepture.com/en/latest/)
- Code highlighter: [Pygments](https://pygments.org/)
### Testing
- [Pytest](https://docs.pytest.org/en/7.2.x/)
### Methodology
- Mobile-first approach
- [BEM nomenclature](https://getbem.com/)
- [Scalable and Modular Architecture for CSS](http://smacss.com/)
- Test Driven Development

## Hopes for the future
Some things that I hope will be implemented in the future, either by me (mochitto) or by the community are:
- [ ] A colorblind-friendly theme
- [ ] An high-contrast theme
- [ ] Any other accessibility improvement
- [ ] Support for more advanced formatting Markdown options
- [ ] [AnkiConnect](https://foosoft.net/projects/anki-connect/) support to make imports automatic
- [ ] An Obsidian addon to run the script/setup the configs from Obsidian
- [ ] Someone making a video about Markdown2Anki, either to just share it or a guide on how it works and how to install it
- [ ] A comprehensive documentation

## Versioning
The formatting of the changelog file is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).
You can [read the CHANGELOG file here](https://github.com/Mochitto/Markdown2Anki/blob/master/CHANGELOG.md).

## License
This project uses the [GPL3 LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt).  
The project was made possible by lots of free software and is a bridge between free softwares; it couldn't have been made possible without [Pygments](https://pygments.org/), [Mistune](https://mistune.lepture.com/en/latest/), [Pytest](https://docs.pytest.org/en/7.2.x/), [esbuild](https://esbuild.github.io/), [sass](https://sass-lang.com/) and tons more of community efforts. 

### Closing note
I hope this project inspires others to create more open source software, fostering growth and collaboration within our community and society.  - Mochitto, 2023
