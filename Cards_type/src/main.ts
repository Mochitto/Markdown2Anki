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

const tab_groups = assertQuerySelectorAll(".tab_group")
for (let tab_group of tab_groups) {
    tab_group.addEventListener("click", set_active_tab)
}

function set_active_tab(event: Event): void {
    let container = event.currentTarget
    let target = event.target
    if (target instanceof Element && container instanceof Element) {
        if (target.classList.contains("tab__label")) {
            for (let tab of container.children) {
                if ([...tab.children].includes(target)) {
                    tab.classList.add("tab--isactive")
                } else {
                    tab.classList.remove("tab--isactive")
                }
            }
        }
    }
}