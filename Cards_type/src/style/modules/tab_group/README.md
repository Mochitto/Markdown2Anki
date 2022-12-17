# Tab group component
## Description
This component is used to display tabs components in a single container.
It pushes all the tabs' bodies to the left, so that they can be un-aligned from their labels.

!!: the contents of the group CAN overflow (both the labels and the bodies), so overflow is to be taken care of by other components

## Classes
- tab_group: creates a flexing context, turns the tabs' bodies to absolutely positioned elements.

## HTML Structure
This sass file is to be used on the following html structure:
```HTML
<main class="tab_group">
    <section class="tab ?tab--isactive?">
        <span class="tab__label">YourLabel</span>
        <div class="tab__body"></div>
    </section>
    <section class="tab ?tab--isactive?">
        <span class="tab__label">YourLabel</span>
        <div class="tab__body"></div>
    </section>
    <!-- Can hold up as many tabs as they can fit-->
</main>
```

## Required variables/extra styling
- Normalizing

## TODO:
- Make labels shrink if overflowing, the same that happens in browsers