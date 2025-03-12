# Welcome to the theme builder for MD2Anki!

This is a small guide meant to help you build your own theme 🐸  
It is supposed to be for complete beginners; let us know with a GitHub issue if you have any trouble with it!  
Happy building 🌸

## How to see your theme 🔍
In this folder there is a `test.html` file, which is a representation of how your card could look inside of Anki.  
You can open this file with your browser (generally it's automatically used if you just `double-click` the file).

Everything will look plain and in black and white but no worries, it's supposed to look like this!  
This will be your canvas 🎨

If you don't need code highlighting, you can simply create a UI theme, without worrying about the Highlight theme.

## Building the UI theme
In the folder `style` there is a file named `UI_theme_template`.  
You should copy this file and name it what you would like your theme to be named, for example `awesome_ui_theme.css`.  
This is a `CSS` file. You will be adding color values to the variables that are present.  
This should give you an idea of how colors work in CSS: https://developer.mozilla.org/en-US/docs/Web/CSS/color.
You can start by adding a color to the `--main-background` variable. 🌸

### Adding `awesome_ui_theme.css` to your html file
Now you can check how the colors are looking.  
To do so, you need to tell the `HTML` file to use your `awesome_ui_theme.css` file as a guide to color the parts of the card.
Open the `test.html` file with a text editor (even word or notepad will do!) and change `<YOUR THEME NAME GOES HERE>` to your file name (`awesome_ui_theme`).  
If you now refresh `test.html` in the browser, you should see your colors!
You can now simply modify the `CSS` file and refresh to see the changes, until you are happy with them 🥳

## Adding the theme to Anki
To add your custom theme to your anki cards, you just need to copy the contents of the `CSS` file and add them to your Anki cards' CSS.  
You can read more on this here: https://docs.ankiweb.net/templates/styling.html#card-styling.  
If you want to share the theme with your friends, you can simply give them the `CSS` file.

## Uploading the theme as an "official" theme (Advanced)
If you want your theme to be part of the supported themes of Markdown2Anki, you need a GitHub account.  
You can follow this guide to learn more about how to contribute to a project: https://docs.github.com/en/get-started/quickstart/contributing-to-projects.  

### Adding your themes to the project

You can then fork the Markdown2Anki repository and add your files under `frontend/src/style/CSS Themes/Highlighting themes` and `UI themes`.  
!! Notice: if your theme covers both UI and highlighting, the files should have the same name.  

### Putting the themes together

You can then add your import statements to the `full_themes` folder, or specify what other files to use (if your theme only covers UI or highlighting).
!! Notice: this file should also be named the same way as your theme.

This is an example of how the import statements file should look:
```css
/* The file should be named the same as your theme. */
@import url("../UI\ Themes/<your theme>.css");
@import url("../Highlighting styles/<your theme>.css");

@import url("../../themeless_main.sass");
```
This is done so that we can later minify your theme and add it to the `themes` folder.

Notice: Always import the `themeless_main.sass` file, as it contains the basic styling for the cards. 

### Last step: Images and readme

As last step, you should add a screen-shot of your theme in the `themes/docs` folder, and add the theme name and the images to the `themes/README.md` file.  
This will help others see your theme when they are browsing them 💕  

!! PLEASE: when adding screenshots, make sure the image is as light as possible while still having ok quality. This will save people's internet connection from downloading huge pictures. Bonus points, if you have multiple pictures, if you can join them together into one, smaller picture.

### Finish! 
Congrats, you've uploaded your theme! 🥳  
There might be things to fix if not everything was done perfectly, but you are very close to having your theme be part of the "official" themes, for everybody to enjoy 💕

Thank you for your help! 💕



## Building the Highlight theme (Advanced)
In the folder `style` there is a file named `Highlight_theme_template.css`.
You should copy this file and name it what you would like your theme to be named, for example `awesome_highlight_theme.css`.  
There are two main parts to this file: 
- The `:root` rule: this is where you can define your palette to use in to highlight the code.
- The `.highlight` specific rules: this is where you add your variables to specify the color of the tokens.

Ideally, you would create new variables (such as `--rose-red: red`) and then add it to the tokens you'd like to have that color:
```css
.highlight .k { color: var(--rose-red); font-weight: bold; } /* Keyword */
```

A list of the meaning of each token can be found here: https://pygments.org/docs/tokens/

!! Notice: How the text is highlighted might not reflect your colors. This could be because the lexer used by pygments (the library that takes care of code highlighting) could be using generic tokens instead of specific ones.

### Dual themes (Advanced)

If you want to create a dual theme, the process is similar to the single theme, but now you also need to add two pairs of UI and Highlighting files (if highlighting is used) in the CSS file in the `full_themes` folder: one for the light mode and one for the dark mode.

For example:
 
```css
/* Import light theme files. */
@import url("../UI\ Themes/<light theme name>.css");
@import url("../Highlighting styles/<light theme name>.css");

/* Import dark theme files. */
@import url("../UI\ Themes/<dark theme name>.css");
@import url("../Highlighting styles/<dark theme name>.css");

/* Import common token file (if applicable. */
@import url("../Highlighting styles/<common tokens>.css");

@import url("../../themeless_main.sass");
```

The main differences are:
* the dark themes should have `.card.nightMode` selector instead of just `.card` selector.
* From organizational perspective is easiest if light and dark themes share the same color name variable and just change hex values.
* It is also the easiest to have a common token file which uses the same color name variables as
defined by both light and dark themes.

For examples see the `catpuccin_latte_and_macchiato.css` and `rose_pine_and_dawn.css` themes

### Checking your highlighting palette
You can link to your `awesome_highlight_theme.css` in the `test.html` file to check the colors.  
If your preferred language is not Javascript and you'd like to see it on your favourite language, the best way to do it is to add the css directly to your Anki cards' CSS.  
If you want, you can even edit the CSS there to have an instant feed-back and then copy back the CSS to the file, if you want to share it with others by contributing.



