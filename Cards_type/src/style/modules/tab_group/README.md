# Tab group component
## Description
This component is used to display tabs components in a single container.
It pushes all the tabs__body-es to the left, so that they can be un-aligned from their labels.

## Classes
- tab_group: creates a flexing context, turns the tabs' bodies to absolutely positioned elements.

## HTML Structure
This sass file is to be used on the following html structure:
```HTML
<main class="tab_group">
    <section class="tab ?tab--isactive?tab--isfullscreen?">
        [...]
    </section>
    <section class="tab ?tab--isactive?tab--isfullscreen?">
        [...]
    </section>
    <!-- Can hold up as many tabs as they can fit-->
</main>
```

## Required variables/extra styling
- Normalizing

