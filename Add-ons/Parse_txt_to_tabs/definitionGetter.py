import requests
import re
import json

# dictionary entry object to organize the word and definitions.
class dictionaryEntry:

    @classmethod
    def fromSearchPage(cls, dataHTML):
        message = ""
        if dataHTML['japanese'][0]:
            # Create div for word, furigana and extra tags
            message += "<div class='jisho-header'>\n"
            
            # Get word (wrapped in a span), either in kanji or kana
            try:
                message += f"<span class='jisho-word'>{dataHTML['japanese'][0]['word']}</span> {dataHTML['japanese'][0]['reading']}\n"
            except KeyError:
                if "reading" in dataHTML['japanese'][0].keys():
                    message += f"<span class='jisho-word'>{dataHTML['japanese'][0]['reading']}</span>\n"
                else: # Usually for Book titles or other media, not really relevant for language learning
                    return

            # Check for tags
            try:
                json_jlpt = dataHTML['jlpt']
                json_common = dataHTML['is_common']
            except KeyError:
                return 

            if json_jlpt or json_common:
                # Create div for flex layout and get tags
                message += "<div class='jisho-header__tags'>\n"
                if json_common:
                    message += f"<span class='jisho-common'>Common word</span>\n"
                if json_jlpt:
                    jlpt_message = " ".join(json_jlpt[0].split("-"))
                    message += f"<span class='jisho-jlpt'>{jlpt_message}</span>\n"
                message += "</div>\n"
            message += "</div>\n"

            # Get meanings and their synonyms 
            senses = dataHTML["senses"]
            for number, sense in enumerate(senses):
                if sense['parts_of_speech'][-1] == "Wikipedia definition": continue
                if number > 2: break # Get only the first three results to avoid cluttering
                message += f"<span class='jisho-category'>{', '.join(sense['parts_of_speech'])}</span>\n"
                definitions = [f"{definition}" for definition in sense["english_definitions"]]
                message += f"{number+1}. {'; '.join(definitions)}\n"
            url = ""
        
        return message

    @classmethod
    def fromEntryPage(cls, name, dataHTML):
        word = re.search(r'"og:title" content="(.+?)の意味',dataHTML,re.DOTALL).group(1)
        reg = re.compile('<div id="jn-.+?_".+?<div class="content-box contents_area meaning_area p10">(.+?)<!-- /contents -->',re.DOTALL)
        shortDef = cleanDefinition(re.search(reg,dataHTML).group(1))
        return cls(name, word, shortDef, "")

    def __init__(self, name, word, shortDef, url):
        self.name = name
        self.shortDef = re.sub(r'<img.+?>|&#x32..;',"",shortDef)
        self.url = url
        self.word = word

    # returns an expanded version of the definition
    def getFullDef(self):
        if self.url == "" or self.shortDef[-3:] != "...":
            return self.shortDef
        else:
            try:
                idNum = self.url.split('#')[-1]
                entryPage = requests.get(self.url).text
                reg = re.compile('<div id="' + idNum + '_".+?<div class="content-box contents_area meaning_area p10">(.+?)<!-- /contents -->',re.DOTALL)
                return cleanDefinition(re.search(reg,entryPage).group(1))
            except requests.exceptions.ConnectionError:
                return self.shortDef

    def __str__(self):
        return self.word+ ": " + self.shortDef

def cleanDefinition(dirty):
    dirtyLines = re.findall(r'<p class="text">.+?</p>|<div class="text">.+?</div>',dirty,re.DOTALL)
    answer = ""
    for line in dirtyLines:
        answer += re.sub(r'<.*?>|&thinsp;|&#x32..;',"",line) + "\n"
    return answer

# Returns the encoding of the word as used in goo辞書's url
def urlEncode(word):
    codedWord = str(word.encode('utf-8'))[2:-1].upper()
    finalized = ""
    for i in range(2, len(codedWord)-1 ,4):
        finalized = finalized + "%" + codedWord[i:i+2]
    return "https://jisho.org/api/v1/search/words?keyword=" + finalized

# searches for the passed word, returning the html of the page
def getSearchPage(word):
    searchPage = requests.get(urlEncode(word))
    searchPage.raise_for_status()
    if not 300 > searchPage.status_code >= 200:
        raise ValueError("Request was not successful")
    return searchPage.json() 

# Returns an array containing dictionaryEntry objects corresponding to the word passed as a parameter
def parseSearch(word): 
    try:
        searchPage = getSearchPage(word)
    except ValueError:
        return ["<strong class='kanji'>失敗</strong><br>Couldn't find" + word + "On jisho.org."]
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        return ["<strong class='kanji'>失敗</strong><br>Couldn't connect to jisho.org"]

    entries = []
    for current, result in enumerate(searchPage["data"]):
        if current > 2:
            break
        entries.append(dictionaryEntry.fromSearchPage(result))
    entries = [entry for entry in entries if entry is not None]
    return ["<hr class='dictionary-separator'>\n".join(entries)]

def test(word):
    print("\n".join(parseSearch(word)))
