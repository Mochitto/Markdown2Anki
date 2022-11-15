# Highlight component
## Description
This component is used to display highlighted code (read only). 
It supports line numbering, line highlighting on hover and text-wrapping.
The resulting component is a block-level element.

## Classes
- highlight: The main container
    - highlight--linenos: an optional state that defines whether or not to have numbered lines
- highlight__language: a label to display the language of the highlighted code
- highlight__code: the container of the highlighted code
- highlight__line: the container of each line 
    - :hover: highlight the line (change background)
    - ::before: line numbers

## HTML Structure
This sass file is to be used on the following html structure:
```HTML
<main class="highlight ?highlight--linenos?">
    <span class="highlight__language">Language</span>
    <div class="highlight__code">
        <pre><code><!-- Added to avoid newlines and style code better
        --><span class="highlight__line"> Your Highlighted code goes here</span><!--
        --><span class="highlight__line"> Your Highlighted code goes here</span><!--
        --></code></pre>
    </div>
</main>
```

## Required variables/extra styling
- All the color coding and styling for the highlighting of the code and code's background (pygments)
- Normalizing (removing default margins and using border-box)