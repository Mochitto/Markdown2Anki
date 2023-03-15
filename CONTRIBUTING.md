# Markdown2Anki dev docs

Welcome to the dev documentation of Markdown2Anki!

This will be high-level, as most details can be found in type-signatures and doc strings in the project, but it should help you understand the general workings and structure of the project!

I suggest to read this while having the file structure open in a tree-view, to get a good idea of the bigger picture.  
If there is any question or suggestion on how to make these docs better, let me know with an issue! :)  

The main guidelines I can give for contributing are:
- Make sure you make type-safe code and use the `common_types` when possible.
- Make sure all tests are passing, unless you voluntarily break them by finding edge cases and want to leave others to fix them.
- When modifying the frontend, make sure all the components work well, also in Anki (sometimes things work outside of it, but not in it...)
- If possible, run the `black` formatter before submitting; most of the parts of this project are formatted with it, so it makes for some nice consistency

Thank you for contributing or even just looking into the project 💕

---

Table of contents

- [Backend](#backend)
  - [Business logic](#business-logic)
  - [Files structure](#files-structure)
    - [Root](#root-level)
    - [Config folder](#config-folder)
    - [Utils](#utils)
    - [Md_2_anki](#md_2_anki)
      - [Utils](#sub-utils)
      - [Process card](#process-card)
      - [Process images](#process-images)
      - [Process clozes](#process-clozes)
  - [Testing](#testing)
  
- [Frontend](#frontend)
  - [Styling](#styling)
  - [Javascript](#javascript)
  - [Building and testing](#building-and-testing)



---

# Backend

## Business logic
When you run the app, the main logic will be:
- Setting up the logger
- Check for updates
- Fetch, merge and validate configurations
- Extract the cards from the markdown input file
- Process each card
  - Check for clozes; if there are any, hash them
  - Extract the different tab labels and tab bodies
  - Compile them into HTML
  - Swap tabs if needed
  - Build the formatted card
  - If there were clozes, re-inject depending on hashes
- Check for images to copy (copy them to the destination if so)
- Divide cards into failed, successful (clozes and basic)
- Output the CSV files

## Files structure
The backend is found in `src/markdown2anki`.  

### Root level
The first files found here are the "top-level" modules.  
- `logger`: takes care of logging and the log file
- `output_handler`: takes care of most of the file writing and copying operations (but the ones that are part of config)
- `main`: This is the file that is running when executing `md2anki`
- `version_check`: takes care of checking for current and latest versions and checking if there was an update

### Config folder
The `config` folder takes care of welcoming the user on the first setup, handling the configurations file, the CLI arguments and general configurations validations and merging.  
It uses the [Type-config](https://pypi.org/project/type-config/) library to handle the creation and parsing of the configurations file and the merging and validation of both the file and the CLI args.   
**Notice:** you can find the `apkg` file here; `config` takes care of handling its own outputs (configurations file and apkg file).

The files are:
- `configs_handle` takes care of handling all of the configs operations: the main function is exposed from this module.
- `first_config` takes care of the first time the user uses the app. It welcomes them, creates a config file at the given directory, an internal file as a "link" to the user's config and an apkg file.
- `parse_args` takes care of parsing CLI arguments
- `config_setup folder`: this is where `type-config` is used to create the configurations options, validations and castings. 

### Utils
The utils folder contains:
- `common_types`: types used through the program; if it's your first time looking at the project, keeping a tab open on this file to read the type signatures might be useful.
- `debug_tools`: holds `expressive_debug`, which allows you to `pprint` or `json.dump` objects to inspect them better. `expressive_debug` is imported in almost all modules to make debugging easier

### Md_2_anki
This sub-package holds the modules that takes care of the card processing.  
The main file processes the given markdown input and returns a dictionary containing much information on the processing of the cards.

The other folders:

#### Sub-Utils
This folder is imported whenever there is a need to use `expressive_debug`, `CardError`, Card-specific types or common types (these to make the sub-package independent from the main package).

#### Process card
This folder takes care of processing a single card.  
The steps they have to go through are divided into their own sub-modules:
- `extract`: finds the tab labels and gets the body by taking the text between tab labels
- `compile`: turns the tab body into HTML using [mistune](https://mistune.lepture.com/en/latest/) and [pygments](https://pygments.org/) with custom modifications
- `format`: takes care of formatting the tabs and the tabs groups (wrapping them in the correct HTML and classes)
- `swap`: takes care of tabs swapping (removing front tabs to be removed and replacing them with back tabs, if there are any)

#### Process Images
This folder takes care of extracting images from formatted cards (the resulting card of the card processing) so that it attempts to find it in the given directory and copy it to the destination directory.

#### Process Clozes
This folder takes care of handling clozes.  

The main steps are:
- Checking if a card has any cloze in it
- Hashing the clozes, so that code-highlighting and compiling to HTML can work as expected
- Re-inject the original clozes, replacing the hashes

The main function of these is so that clozes are picked up correctly by Anki: Anki doesn't like when clozes are split up by HTML, so this method ensures that all clozes don't have any HTML tags between any of their parts.

## Testing
The project used a Test Driven Development approach starting from half of its development, so the tests should cover a lot of cases (hopefully).  
They follow the same structure as the main project; if you look for tests on a specific part or function, you should be able to find them in the same (or almost the same) folder, just starting from `tests`.  

The project uses [pytest](https://docs.pytest.org) for testing.

A couple of unique parts:
- `assets` are files used to test output functions or make sure that file handling works as expected
- `conftest` sets up a temporary folder for the same reason
- `setup folder` takes care of creating different configurations files to test configuration handling and integration tests 

---

# Frontend
You can find all that has to do with the "frontend" of the project (the styling and script bundled in the Anki note types) in the `frontend` folder.  
There are some dev-dependencies that you need to be able to properly test and build the files, so you should run (make sure that your cwd is the `frontend` folder):
```bash
npm install 
```

The frontend is built with Typescript and Sass files.  

## Styling
You can find all of the stylings in `src/style`.
The most important files are:
- `main.sass` - This is the file that is built into the Note types styling. Ships the "Rose pine" theme by default
- `themeless_main.sass` - This is the file used for the Theme builder, which lacks themes.
- `base.sass` - Base styles applied to tags.
- `layout.sass` - Utility classes for basic layouts.
There are some folders as well:
- `modules` - this folder holds the main modules that build up the note type. Those are `tab`, `highlight` and `tab group`
  - `tab` takes care of the tabs, from the label to the content
  - `highlight` takes care of the code blocks
  - `tab group` takes care of grouping the tabs
- `utilities` - this folder holds a normalizer and takes care of setting the root font size to 62.5% (10px)
- `CSS Themes` - this folder holds all of the themes, divided in UI and Highlight. 
  - `full_themes` - this folder holds files that simply import and bundle together a UI and Highlight theme. These are minified and sent to the root's `themes` folder upon building

The styling follows a mobile-first approach, media queries are based on screen orientation instead of pixels.  
The classes nomenclature follows BEM principles, the architecture SMACSS methodology.  

## Javascript

The javascript file is built from a Typescript file that is in `src/main.ts`.  
The script takes care of the interactivity aspect of the note types.  

Some particular aspects are:
- Some elements are extracted from the DOM upon event trigger; this is not optimal, but it had to be done due to how Anki treats its DOM: the HTML isn't built on each card, but modified, so if you extract all of your elements when you first load the page, the buttons won't work anymore after the first card.
- The class "nightMode" is applied to the root/HTML element: this is done so that you can style themes using `:root.nightMode`, and use the colors across the whole note type without having to worry about complex selectors.

## Building and testing

To test the styling and script, you can run
```bash
npm run watch
```
This will build your style from `main.sass` and script from `main.ts` and spin up a live server, that will refresh on each change of sass, css or ts files.

Calling `npm run build` will also build themes and `themeless_main.sass` for the theme builder so that all of these files are always up to date.
