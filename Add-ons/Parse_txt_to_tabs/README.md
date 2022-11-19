# AnkiAutoDefine

An anki add-on for automatic Japanese-to-Japanese dictionary generation using the [goo.ne 国語辞書](https://dictionary.goo.ne.jp/jn/)

Recommended to be used with the Japanese Support add on or MIA add on, but is functional on its own.

The add on will search the source field for bold words and search for a match.
These words and their definitions are then automatically added in the destination field if it is empty.
If more than one is found, you will be able to select from the first page of results.
If you still cannot find the correct definition, you must search manually.

The add on works out of the box with the Japanese recognition card type from the Japanese Support add-on, as well as the MIA card type from the MIA add-on.

If you would like to add support to a new card type, open the config.json file and add a new card type in the following syntax. 
This can also be accessed within anki by going to the add-on menu and opening this add-ons settings. Start up anki and the add on should now work on your cards. You must enter the card an field names exactly or you will have errors (nothing dangerous, at the worst it will just shut down the add-on until you restart anki)

```javascript
{"name" : "(the name of the card type)",
"src" : "(the name of the field in the card to scan for bold words)",
"dst" : "(Name of the field where the definition should be placed)"}
```

Link to anki add-on page: https://ankiweb.net/shared/info/1202751671
