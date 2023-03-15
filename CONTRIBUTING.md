# Markdown2Anki dev docs

Welcome to the dev documentation of Markdown2Anki!

This will be high-level, as most details can be found in type-signatures and doc strings in the project, but it should give you some help understanding the general working and structure of the project!

---

Table of contents

- [Backend](#backend)

- [Frontend](#frontend)
  - [Styling](#styling)
  - [Javascript](#javascript)
  - [Building and testing](#building-and-testing)

---

# Backend

---

# Frontend
You can find all that has to do with the "frontend" of the project (the styling and script that is bundled in the Anki note types) in the `frontend` folder.  
There are some dev-dependencies that you need to be able to properly test and build the files, so you should run (make sure that your cwd is the `frontend` folder):
```bash
npm install 
```

The frontend is built with Typescript and Sass files.  

## Styling
You can find all of the styling in `src/style`.
The most important files are:
- `main.sass` - This is the file that is built into the Note types styling. Ships the "Rose pine" theme by default
- `themeless_main.sass` - This is the file used for the Theme builder, lacks themes.
- `base.sass` - Base styles applied to tags.
- `layout.sass` - Utility classes for basic layouts.
There are some folders as well:
- `modules` - this folder holds the main modules that build up the note type. Those are `tab`, `highlight` and `tab group`
  - `tab` takes care of the tabs, from the label to the content
  - `highlight` takes care of the code blocks
  - `tab group` takes care of grouping the tabs
- `utiliites` - this folder holds a normalizer and takes care of setting the root font size to 62.5% (10px)
- `CSS Themes` - this folder holds all of the themes, divided in UI and Highlight. 
  - `full_themes` - this folder holds files that simply import and bundle together a UI and Highlight theme. These are minified and sent to the root's `themes` folder upon building

The styling follows a mobile-first approach and media queries are based on screen orientation instead of pixels.  
The classes nomenclature follows BEM principles, the architecture SMACSS methodology.  

## Javascript

The javascript file is built from a Typescript file that is in `src/main.ts`.  
The script takes care of the interactivity aspect of the note types.  

Some particular aspects, are:
- Some elements are extracted from the DOM upon event trigger; this is not optimal, but had to be done due to how Anki treats its DOM: the HTML isn't built on each card, but modified, so if you extract all of your elements when you first load the page, the buttons won't work anymore after the first card.
- The class "nightMode" is applied to the root/HTML element: this is done so that you can style themes using `:root.nightMode`, and use the colors across the whole note type, without having to worry about complex selectors.

## Building and testing

To test the styling and script you can run
```bash
npm run watch
```
This will build your style from `main.sass` and script from `main.ts` and spin up a live server, that will refresh on each change of sass, css or ts files.

Calling `npm run build` will, on the other hand, also build themes and `themeless_main.sass` for the theme builder, so that all of these files are always up to date.
