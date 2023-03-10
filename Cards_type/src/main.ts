function assertQuerySelectorAll(query: string) {
    let error_message = `<h1 style="text-size: 3rem;">ERROR: Couldn't find any element using the query: "${query}".</h1>
    <p>Make sure there were no errors in your markdown.<br>If you need help, please contact the developers by writing an issue at <a href="https://github.com/Mochitto/Anki-code-Cards">our GitHub page</a></p>`
    let element = document.querySelectorAll(query)
    if (!element.length) {
        document.body.innerHTML = error_message;
        throw new Error(`Couldn't find any element matching ${query}`)
        }
    return element
}
const nightMode = document.querySelector(".nightMode")
if (nightMode) {
    document.documentElement.classList.add("nightMode")
}


const tab_groups = assertQuerySelectorAll(".tab_group")
// tabs, tabs_labels are defined on event call since anki
// reuses the same html if the note type is the same; it just
// changes the differences.
let tabs: NodeListOf<Element>
let tabs_labels: NodeList 

let tab_to_restore: Element
let tab_that_went_fullscreen: Element

for (let tab_group of tab_groups) {
    tab_group.addEventListener("click", handle_clicks)
}

// Add a keydown event listener to the window object
window.addEventListener("keydown", function(event) {
  // This handles short-keys, by activating the tab 
  // That has a matching number as the one pressed
  tabs_labels = assertQuerySelectorAll(".tab__label")
  if (event.altKey && /^[0-9]$/.test(event.key)) {
    let index = parseInt(event.key) - 1
    let button = tabs_labels[index] 
    if (button instanceof HTMLButtonElement) { 
    button.click()}
  }
});

function handle_clicks(event: Event): void {
    event.preventDefault()
    let container = event.currentTarget
    let target = event.target
    if (target instanceof HTMLSpanElement) {
        target = target.parentElement
    }
    if (!(target instanceof Element && container instanceof Element && target.classList.contains("tab__label"))) {
        return
    } 
    tabs = assertQuerySelectorAll(".tab")
    let tab = target.parentElement
    if (tab?.classList.contains("tab--isfullscreen")) {
        restoreActiveTabs(tab)
    }
    else if (tab?.classList.contains("tab--isactive")) {
        setFullscreenTab(tab)
    } else {
        setActiveTab(target, container)
    }
}

function restoreActiveTabs(fullscreen_tab: Element) {
    fullscreen_tab.classList.add("tab--isactive")
    fullscreen_tab.classList.remove("tab--isfullscreen")
    if (tab_to_restore?.parentElement == fullscreen_tab.parentElement) {
        tab_that_went_fullscreen.classList.add("tab--isactive")
    } else {
        tab_to_restore?.classList.add("tab--isactive")

    }
}

function setFullscreenTab(tab: Element) {
    tab.classList.remove("tab--isactive")
    tab.classList.add("tab--isfullscreen")
    for (let other_tab of tabs) {
        if (other_tab.classList.contains("tab--isactive")) {
            tab_to_restore = other_tab
            tab_that_went_fullscreen = tab
            other_tab.classList.remove("tab--isactive")
        }
    }
}

function setActiveTab(target: Element, container: Element) {
        let fullscreen_tab = document.querySelector(".tab--isfullscreen")
        for (let tab of container.children) {
            tab.classList.remove("tab--isactive")
            tab.classList.remove("tab--isfullscreen")
        }

        if (fullscreen_tab) {
            fullscreen_tab.classList.remove("tab--isfullscreen")
            target.parentElement?.classList.add("tab--isfullscreen")
        } else {
            target.parentElement?.classList.add("tab--isactive")
        }
    }
