# Tab component
## Description
This component is used to display content with a label on top, which is useful when working with multiple blocks that should take up the whole viewport (one at the time) or to group and highlight content.
Tabs' bodies are by default hidden and are shown only when applying the state "tab--isactive" (to accomodate use within tabs groups).
They can also become "full-screen" with the state "tab--isfullscreen".

## Classes
- tab
    - tab--isactive: changes the label's styling and shows the body
    - tab--isfullscreen: changes the label's styling and makes the body take up the whole screen.
- tab__label: a button describing the content of the tab
- tab__body: the container of the content of the tab
    -tab__body__content: the content of the tab
    - scrollbar/scrollbar-thumb: always showing, added for aesthetic reasons 

## HTML Structure
This sass file is to be used on the following html structure:
```HTML
<main class="tab ?tab--isactive?">
    <button class="tab__label"><span>YourLabel</span></button>
    <div class="tab__body">
        <div class="tab__body__content">
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Doloribus, atque reiciendis. Amet perspiciatis veritatis molestias. Error fugiat ea numquam! Voluptatem fugit porro ducimus, earum excepturi aut in libero consequatur quae!</p>
        </div>
    </div>
</main>
```

## Required variables/extra styling
- Normalizing (removing default margins and using border-box)
