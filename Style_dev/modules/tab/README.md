# Tab component
## Description
This component is used to display content with a label on top, which is useful when working with multiple blocks that should take up the whole viewport (one at the time) or to group and highlight content.
Tabs' bodies are by default hidden and are shown only when applying the state "tab--isactive" (to accomodate use within tabs groups).

## Classes
- tab
    - tab--isactive: changes the label's styling and shows the body
- tab__label: a span describing the content of the tab
- tab__body: the content of the tab
    - scrollbar/scrollbar-thumb: always showing, added for aesthetic reasons 

## HTML Structure
This sass file is to be used on the following html structure:
```HTML
<main class="tab ?tab--isactive?">
    <span class="tab__label">YourLabel</span>
    <div class="tab__body">
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Doloribus, atque reiciendis. Amet perspiciatis veritatis molestias. Error fugiat ea numquam! Voluptatem fugit porro ducimus, earum excepturi aut in libero consequatur quae!</p>
    </div>
</main>
```

## Required variables/extra styling
- Normalizing (removing default margins and using border-box)

## TODO:
- Fix color styling