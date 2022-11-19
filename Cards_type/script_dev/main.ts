console.log("hello")
/*
1. Parse fields
    1.1: Get tabs containers (there could be no second tab group; select them together and iterate through array)
    1.2: Exculde code blocks (<section class="highlight highlight--linenos">[\s\S]+?<\/code><\/pre><\/div><\/section>(?:<br>)?)
    1.3  Match links and replace them with compiled HTML \[([\s\S]+?)\]\(([\s\S]+?\))
        as <a ref="group2">group1</a>
    1.4: Check if |:| in the text:
        if so: 
            - Append \n\n to the end of the file to account for bad formatting
            - match ^([\s\S]*?)\|:\|([\s\S]+?)\n\n+
            - And store as: {
                label: group1 || Prompt/Answer/Explanation etc... Depending on field 
                body: group2
              } In the fieldsArray: objects[]
        else:
            store object: [{
                label: Prompt/Answer/Explanation etc... Depending on field
                body: text
            }]

2. Compile them to HMTL
    - Iterate through the fieldsArray/s
    - Wrap data in matching HTML tags

3. Inject back into cards' fields
*/
