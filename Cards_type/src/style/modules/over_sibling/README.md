# Over sibling utility module
## Description
This utility module (.u-something) is used to hide the direct sibling of the element that has the class ".u-over_sibling".
This is done by making the element absolutely positioned and lifting it, while maintaining the sibling's position.
The sibling element's opacity is also reduced, to highlight the change.

The two elements need to be in a flexing context that takes up all the viewport and they should take 50% of the screen for the class to work properly.

## Classes
- .u-over_sibling: the element that will be put over the siblings
    - :hover: turn the element to absolute and lift it over the sibling. Keep the sibling in place using margin auto.
    - :after: Add a small label signaling the possiblity of going back to seeing the other sibling in the bottom right of the corner. Hidden by default.
    - :hover:after: show the small label.

## HTML Structure
This sass file is to be used on the following html structure:
```HTML
<main class="FlexContainer AsBigAsViewport">
    <div class="u-over_sibling"></div>
    <div></div>
</main>
```

## Required variables/extra styling
- Normalizing 